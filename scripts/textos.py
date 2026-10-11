"""Textos que se incrustan en el dashboard (títulos, datos del estudiante y análisis crítico)."""

TITULO = "Dashboard de Eficiencia de Red Distribuidora y Costos Logísticos"

DATOS_ESTUDIANTE = "Estudiante: [Apellido Nombre]   |   Fecha: [dd/mm/aaaa]   |   Nivel: [Nivel]"

ANALISIS_TITULO = "Análisis crítico"

ANALISIS = [
    "La región Oeste es la que presenta ineficiencias críticas de entrega: tiene el costo de envío promedio "
    "más alto (USD 3,297.50; 67 % más que Este, con USD 1,972.14) y, aun así, el mayor tiempo promedio de "
    "entrega (4.87 días frente a 3.28 en Este). La ineficiencia se repite en ambos servicios: su Express cuesta "
    "en promedio USD 4,415 (49 % más que el Express de Este) pero tarda 2.55 días (84 % más que los 1.38 días "
    "de Este), y su Estándar tarda 7.19 días con un costo 78 % mayor que el Estándar de Este.",

    "En la nube de dispersión se forman dos grupos: Estándar (USD 1,100–2,300; 4.5–7.5 días) y Express "
    "(USD 2,800–4,600; 1.3–2.8 días). La línea de tendencia tiene pendiente negativa (≈ −1.3 días por cada "
    "USD 1,000 adicionales): el Express sí reduce el tránsito (de 5.83 a 1.95 días, con un sobrecosto de "
    "≈ USD 561 por día ahorrado). Pero dentro de cada grupo la relación se invierte: los envíos más caros "
    "también son los más lentos. Los valores atípicos se ubican en el extremo superior derecho de cada nube y "
    "son del Oeste —pedidos 1022 (USD 2,300; 7.5 días) y 1023 (USD 4,600; 2.8 días)—, con las burbujas más "
    "grandes (ventas de hasta USD 25,100): la región que más vende y más paga por envío es la que recibe el "
    "peor servicio. Se recomienda auditar rutas, transportistas y bodegas del Oeste antes de ampliar allí "
    "el uso del Express.",
]
