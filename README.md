# miguel
base de datos

## Práctica: visualizaciones complejas en Power BI

**Caso:** análisis de eficiencia logística en e-commerce (asignatura Visualización de Datos).

| Carpeta / archivo | Contenido |
|---|---|
| [`GUIA_PASO_A_PASO.md`](GUIA_PASO_A_PASO.md) | **Empieza aquí.** Cómo abrir el proyecto ya armado o construirlo a mano, y cómo publicar y compartir el vínculo. |
| `powerbi/` | Proyecto de Power BI Desktop (`Practica_V_Complejas.pbip`) con el modelo y el dashboard completo: dispersión con tendencia, gráfico mixto con promedios y eje dual, 2 segmentaciones, 2 tarjetas, título, datos del estudiante y análisis. |
| `datos/` | Dataset piloto de 60 registros (`Logistica_Global.xlsx` y `.csv`), con los tipos correctos, listo para *Especificar datos*. |
| [`analisis/ANALISIS_CRITICO.md`](analisis/ANALISIS_CRITICO.md) | Párrafo conclusivo para el reporte y las cifras que lo respaldan. |
| `analisis/vista_previa_resultados.png` | Resultados esperados (generados con Python) para comparar con lo que muestre Power BI. |
| `scripts/` | Scripts de Python que generan todo lo anterior: `generar_datos.py`, `generar_pbip.py` y `generar_vista_previa.py`. |

### Conclusión principal

La región **Oeste** tiene el mayor costo de envío promedio (USD 3,297.50) y, aun así, el mayor tiempo de entrega (4.87 días). En la dispersión, sus pedidos son los atípicos del extremo superior derecho de cada nube: pedidos 1022 y 1023.

### Pendiente para el estudiante

1. Abrir el `.pbip` en Power BI Desktop, pulsar **Actualizar** y escribir nombre, fecha y nivel.
2. Guardar como `Apellido_Nombre_Practica V_Complejas.pbix`.
3. Iniciar sesión, **Publicar** en *Mi área de trabajo*, copiar el vínculo y pegarlo en el aula virtual.

### Regenerar los archivos

```bash
pip install openpyxl pandas matplotlib
cd scripts
python3 generar_datos.py && python3 generar_pbip.py && python3 generar_vista_previa.py
```
