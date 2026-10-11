"""Genera el proyecto de Power BI (formato PBIP) con el modelo y el dashboard de la práctica.

Estructura generada en powerbi/:
  Practica_V_Complejas.pbip
  Practica_V_Complejas.SemanticModel/   (modelo: tabla Logistica_Global con los 60 registros)
  Practica_V_Complejas.Report/          (reporte en formato PBIR: 1 página con 9 objetos visuales)
"""
import hashlib
import json
import shutil
import uuid
from pathlib import Path

from datos import FILAS, MESES
from textos import ANALISIS, ANALISIS_TITULO, DATOS_ESTUDIANTE, TITULO

PROYECTO = "Practica_V_Complejas"
TABLA = "Logistica_Global"
RAIZ = Path(__file__).resolve().parent.parent / "powerbi"
SCHEMAS = "https://developer.microsoft.com/json-schemas/fabric"
TEMA_BASE = "CY24SU06"
TEMA_PROPIO = "Logistica.json"
VERSION_TEMA = "5.56"
# Tema base estándar de Power BI (copiado de la plantilla PBIR de semantic-link-labs, licencia MIT)
TEMA_BASE_ORIGEN = Path(__file__).resolve().parent / "recursos" / f"{TEMA_BASE}.json"

# Paleta categórica (Estándar = azul, Express = naranja; el orden alfabético de la leyenda los asigna así)
COLORES = ["#2A78D6", "#EB6834", "#1BAF7A", "#EDA100", "#E87BA4", "#008300", "#6250D6", "#E34948"]
TINTA = "#0B0B0B"
TINTA_2 = "#52514E"

SUMA, PROMEDIO = 0, 1


def guid(semilla):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"{PROYECTO}/{semilla}"))


def nombre_visual(semilla):
    return hashlib.sha1(semilla.encode()).hexdigest()[:20]


def escribir(ruta, contenido):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(contenido, str):
        ruta.write_text(contenido, encoding="utf-8")
    else:
        ruta.write_text(json.dumps(contenido, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- modelo semántico

def expresion_m():
    filas = ",\n".join(
        f'            {{{i}, "{mes}", "{reg}", "{tipo}", {ven}, {cos}, {dias}}}'
        for i, mes, reg, tipo, ven, cos, dias in FILAS
    )
    meses = ", ".join(f'"{m}"' for m in MESES)
    texto = f"""let
    Origen = #table(
        type table [
            ID_Pedido = Int64.Type,
            Mes = text,
            #"Región" = text,
            Tipo_Envio = text,
            Ventas_USD = Int64.Type,
            Costo_Envio_USD = Int64.Type,
            Dias_Entrega = number
        ],
        {{
{filas}
        }}
    ),
    #"Mes ordenado" = Table.AddColumn(Origen, "Mes_Num", each List.PositionOf({{{meses}}}, [Mes]) + 1, Int64.Type)
in
    #"Mes ordenado\""""
    return texto.split("\n")


def columna(nombre, tipo, resumen="none", formato=None, **extra):
    c = {"name": nombre, "dataType": tipo}
    if formato:
        c["formatString"] = formato
    c.update(extra)
    c["lineageTag"] = guid(f"col/{nombre}")
    c["summarizeBy"] = resumen
    c["sourceColumn"] = nombre
    c["annotations"] = [{"name": "SummarizationSetBy", "value": "User"}]
    return c


def modelo():
    return {
        "compatibilityLevel": 1567,
        "model": {
            "culture": "es-MX",
            "dataAccessOptions": {"legacyRedirects": True, "returnErrorValuesAsNull": True},
            "defaultPowerBIDataSourceVersion": "powerBI_V3",
            "sourceQueryCulture": "es-MX",
            "tables": [
                {
                    "name": TABLA,
                    "lineageTag": guid("tabla"),
                    "columns": [
                        columna("ID_Pedido", "int64", formato="0"),
                        columna("Mes", "string", sortByColumn="Mes_Num"),
                        columna("Región", "string"),
                        columna("Tipo_Envio", "string"),
                        columna("Ventas_USD", "int64", "sum", "\\$#,0;(\\$#,0);\\$#,0"),
                        columna("Costo_Envio_USD", "int64", "sum", "\\$#,0;(\\$#,0);\\$#,0"),
                        columna("Dias_Entrega", "double", "sum", "#,0.00"),
                        columna("Mes_Num", "int64", formato="0", isHidden=True),
                    ],
                    "partitions": [
                        {
                            "name": TABLA,
                            "mode": "import",
                            "source": {"type": "m", "expression": expresion_m()},
                        }
                    ],
                    "annotations": [{"name": "PBI_ResultType", "value": "Table"}],
                }
            ],
            "annotations": [
                {"name": "PBI_QueryOrder", "value": json.dumps([TABLA])},
                {"name": "__PBI_TimeIntelligenceEnabled", "value": "0"},
            ],
        },
    }


# ---------------------------------------------------------------- reporte (PBIR)

def lit(valor):
    return {"expr": {"Literal": {"Value": valor}}}


def texto_lit(s):
    return lit("'" + s.replace("'", "''") + "'")


def color(hex_):
    return {"solid": {"color": texto_lit(hex_)}}


def campo(prop):
    return {"Column": {"Expression": {"SourceRef": {"Entity": TABLA}}, "Property": prop}}


def proy_columna(prop):
    return {"field": campo(prop), "queryRef": f"{TABLA}.{prop}", "nativeQueryRef": prop, "active": True}


def proy_agregado(prop, funcion):
    prefijo, nombre = {SUMA: ("Sum", "Suma de"), PROMEDIO: ("Avg", "Promedio de")}[funcion]
    return {
        "field": {"Aggregation": {"Expression": campo(prop), "Function": funcion}},
        "queryRef": f"{prefijo}({TABLA}.{prop})",
        "nativeQueryRef": f"{nombre} {prop}",
    }


def titulo_visual(texto):
    return {
        "title": [
            {
                "properties": {
                    "show": lit("true"),
                    "text": texto_lit(texto),
                    "fontSize": lit("12D"),
                    "bold": lit("true"),
                    "fontColor": color(TINTA),
                }
            }
        ]
    }


def contenedor(semilla, x, y, w, h, z, visual):
    return {
        "$schema": f"{SCHEMAS}/item/report/definition/visualContainer/1.1.0/schema.json",
        "name": nombre_visual(semilla),
        "position": {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": z},
        "visual": visual,
    }


def cuadro_texto(parrafos):
    return {
        "visualType": "textbox",
        "objects": {"general": [{"properties": {"paragraphs": parrafos}}]},
        "drillFilterOtherVisuals": True,
    }


def corrida(valor, tam, negrita=False, col=TINTA):
    estilo = {"fontSize": f"{tam}pt", "color": col}
    if negrita:
        estilo["fontWeight"] = "bold"
    return {"value": valor, "textStyle": estilo}


def visuales():
    v = []

    # 1. Título del dashboard
    v.append(contenedor("titulo", 20, 8, 1240, 44, 0, cuadro_texto([
        {"textRuns": [corrida(TITULO, 20, negrita=True)], "horizontalTextAlignment": "center"},
    ])))

    # 2. Datos del estudiante (editar en Power BI Desktop)
    v.append(contenedor("estudiante", 20, 52, 1240, 30, 1, cuadro_texto([
        {"textRuns": [corrida(DATOS_ESTUDIANTE, 11, col=TINTA_2)], "horizontalTextAlignment": "center"},
    ])))

    # 3. Segmentador: Mes (lista desplegable)
    v.append(contenedor("slicer_mes", 20, 92, 290, 96, 2, {
        "visualType": "slicer",
        "query": {"queryState": {"Values": {"projections": [proy_columna("Mes")]}}},
        "objects": {
            "data": [{"properties": {"mode": texto_lit("Dropdown")}}],
            "selection": [{"properties": {"selectAllCheckboxEnabled": lit("true")}}],
            "header": [{"properties": {"show": lit("true")}}],
        },
        "drillFilterOtherVisuals": True,
    }))

    # 4. Segmentador: Tipo_Envio (lista)
    v.append(contenedor("slicer_tipo", 326, 92, 290, 96, 3, {
        "visualType": "slicer",
        "query": {"queryState": {"Values": {"projections": [proy_columna("Tipo_Envio")]}}},
        "objects": {
            "data": [{"properties": {"mode": texto_lit("Basic")}}],
            "selection": [{"properties": {"selectAllCheckboxEnabled": lit("true")}}],
            "header": [{"properties": {"show": lit("true")}}],
        },
        "drillFilterOtherVisuals": True,
    }))

    # 5 y 6. Tarjetas KPI (el título del visual reemplaza a la etiqueta de categoría para no repetir texto)
    for semilla, x, z, prop, funcion, titulo, decimales in [
        ("card_ventas", 632, 4, "Ventas_USD", SUMA, "Ventas totales (USD)", "0L"),
        ("card_dias", 948, 5, "Dias_Entrega", PROMEDIO, "Promedio general de días de entrega", "2L"),
    ]:
        v.append(contenedor(semilla, x, 92, 312, 96, z, {
            "visualType": "card",
            "query": {"queryState": {"Values": {"projections": [proy_agregado(prop, funcion)]}}},
            "objects": {
                "labels": [{"properties": {
                    "labelDisplayUnits": lit("1D"),
                    "labelPrecision": lit(decimales),
                    "fontSize": lit("28D"),
                    "color": color(TINTA),
                }}],
                "categoryLabels": [{"properties": {"show": lit("false")}}],
            },
            "visualContainerObjects": titulo_visual(titulo),
            "drillFilterOtherVisuals": True,
        }))

    # 7. Gráfico de dispersión: X = costo, Y = días, detalle = pedido, leyenda = tipo, tamaño = ventas
    v.append(contenedor("dispersion", 20, 198, 744, 318, 6, {
        "visualType": "scatterChart",
        "query": {"queryState": {
            "Category": {"projections": [proy_columna("ID_Pedido")]},
            "Series": {"projections": [proy_columna("Tipo_Envio")]},
            "X": {"projections": [proy_agregado("Costo_Envio_USD", SUMA)]},
            "Y": {"projections": [proy_agregado("Dias_Entrega", SUMA)]},
            "Size": {"projections": [proy_agregado("Ventas_USD", SUMA)]},
        }},
        "objects": {
            "legend": [{"properties": {"show": lit("true"), "position": texto_lit("Top")}}],
            "trend": [{"properties": {
                "show": lit("true"),
                "lineColor": color(TINTA_2),
            }}],
        },
        "visualContainerObjects": titulo_visual("Costo de envío vs. días de entrega por pedido (tamaño = ventas)"),
        "drillFilterOtherVisuals": True,
    }))

    # 8. Gráfico mixto (columnas + línea) con eje dual: promedio de costo y promedio de días por región
    v.append(contenedor("mixto", 780, 198, 480, 318, 7, {
        "visualType": "lineClusteredColumnComboChart",
        "query": {"queryState": {
            "Category": {"projections": [proy_columna("Región")]},
            "Y": {"projections": [proy_agregado("Costo_Envio_USD", PROMEDIO)]},
            "Y2": {"projections": [proy_agregado("Dias_Entrega", PROMEDIO)]},
        }},
        "objects": {
            "labels": [{"properties": {"show": lit("true")}}],
            "legend": [{"properties": {"show": lit("true"), "position": texto_lit("Top")}}],
            "valueAxis": [{"properties": {"secShow": lit("true")}}],
        },
        "visualContainerObjects": titulo_visual("Costo promedio (USD) y días promedio de entrega por región"),
        "drillFilterOtherVisuals": True,
    }))

    # 9. Párrafo de análisis crítico
    parrafos = [{"textRuns": [corrida(ANALISIS_TITULO, 12, negrita=True)]}]
    parrafos += [{"textRuns": [corrida(p, 10)]} for p in ANALISIS]
    v.append(contenedor("analisis", 20, 526, 1240, 186, 8, cuadro_texto(parrafos)))

    return v


def tema():
    return {
        "name": "Logistica",
        "dataColors": COLORES,
        "foreground": TINTA,
        "foregroundNeutralSecondary": TINTA_2,
        "background": "#FFFFFF",
        "tableAccent": COLORES[0],
        "good": "#0CA30C",
        "neutral": "#FAB219",
        "bad": "#D03B3B",
        "maximum": COLORES[0],
        "center": "#F0EFEC",
        "minimum": "#E34948",
    }


def generar():
    if RAIZ.exists():
        shutil.rmtree(RAIZ)
    modelo_dir = RAIZ / f"{PROYECTO}.SemanticModel"
    reporte_dir = RAIZ / f"{PROYECTO}.Report"
    definicion = reporte_dir / "definition"
    pagina = "e1f0c3a7b2d94c18a6d5"

    escribir(RAIZ / f"{PROYECTO}.pbip", {
        "$schema": f"{SCHEMAS}/pbip/pbipProperties/1.0.0/schema.json",
        "version": "1.0",
        "artifacts": [{"report": {"path": f"{PROYECTO}.Report"}}],
        "settings": {"enableAutoRecovery": True},
    })
    escribir(RAIZ / ".gitignore", "**/.pbi/localSettings.json\n**/.pbi/cache.abf\n")

    # Modelo semántico
    escribir(modelo_dir / ".platform", {
        "$schema": f"{SCHEMAS}/gitIntegration/platformProperties/2.0.0/schema.json",
        "metadata": {"type": "SemanticModel", "displayName": PROYECTO},
        "config": {"version": "2.0", "logicalId": guid("semanticmodel")},
    })
    escribir(modelo_dir / "definition.pbism", {
        "$schema": f"{SCHEMAS}/item/semanticModel/definitionProperties/1.0.0/schema.json",
        "version": "1.0",
        "settings": {},
    })
    escribir(modelo_dir / "model.bim", modelo())

    # Reporte
    escribir(reporte_dir / ".platform", {
        "$schema": f"{SCHEMAS}/gitIntegration/platformProperties/2.0.0/schema.json",
        "metadata": {"type": "Report", "displayName": PROYECTO},
        "config": {"version": "2.0", "logicalId": guid("report")},
    })
    escribir(reporte_dir / "definition.pbir", {
        "$schema": f"{SCHEMAS}/item/report/definitionProperties/1.0.0/schema.json",
        "version": "4.0",
        "datasetReference": {"byPath": {"path": f"../{PROYECTO}.SemanticModel"}},
    })
    temas = reporte_dir / "StaticResources"
    escribir(temas / "SharedResources" / "BaseThemes" / f"{TEMA_BASE}.json", TEMA_BASE_ORIGEN.read_text(encoding="utf-8"))
    escribir(temas / "RegisteredResources" / TEMA_PROPIO, tema())
    escribir(definicion / "version.json", {
        "$schema": f"{SCHEMAS}/item/report/definition/versionMetadata/1.0.0/schema.json",
        "version": "2.0.0",
    })
    escribir(definicion / "report.json", {
        "$schema": f"{SCHEMAS}/item/report/definition/report/1.1.0/schema.json",
        "themeCollection": {
            "baseTheme": {"name": TEMA_BASE, "reportVersionAtImport": VERSION_TEMA, "type": "SharedResources"},
            "customTheme": {"name": TEMA_PROPIO, "reportVersionAtImport": VERSION_TEMA, "type": "RegisteredResources"},
        },
        "layoutOptimization": "None",
        "objects": {"section": [{"properties": {"verticalAlignment": texto_lit("Top")}}]},
        "resourcePackages": [
            {
                "name": "SharedResources",
                "type": "SharedResources",
                "items": [{"name": TEMA_BASE, "path": f"BaseThemes/{TEMA_BASE}.json", "type": "BaseTheme"}],
            },
            {
                "name": "RegisteredResources",
                "type": "RegisteredResources",
                "items": [{"name": TEMA_PROPIO, "path": TEMA_PROPIO, "type": "CustomTheme"}],
            },
        ],
        "settings": {
            "useStylableVisualContainerHeader": True,
            "defaultDrillFilterOtherVisuals": True,
            "allowChangeFilterTypes": True,
            "useEnhancedTooltips": True,
            "useDefaultAggregateDisplayName": True,
        },
    })
    escribir(definicion / "pages" / "pages.json", {
        "$schema": f"{SCHEMAS}/item/report/definition/pagesMetadata/1.0.0/schema.json",
        "pageOrder": [pagina],
        "activePageName": pagina,
    })
    escribir(definicion / "pages" / pagina / "page.json", {
        "$schema": f"{SCHEMAS}/item/report/definition/page/1.1.0/schema.json",
        "name": pagina,
        "displayName": "Dashboard Logístico",
        "displayOption": "FitToPage",
        "height": 720,
        "width": 1280,
    })
    for vis in visuales():
        escribir(definicion / "pages" / pagina / "visuals" / vis["name"] / "visual.json", vis)

    print("OK:", RAIZ)


if __name__ == "__main__":
    generar()
