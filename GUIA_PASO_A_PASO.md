# Práctica: visualizaciones complejas en Power BI (eficiencia logística)

Hay dos formas de hacer la práctica:

- **Opción A (rápida):** abrir el proyecto ya armado (`powerbi/Practica_V_Complejas.pbip`), actualizar los datos, poner tus datos personales y guardarlo como `.pbix`.
- **Opción B (manual):** construir el dashboard desde cero siguiendo la guía del docente. Sirve como respaldo si la opción A no abre, y para entender cada paso.

En los dos casos terminas con el **Paso 5** (publicar y compartir el vínculo), que solo puedes hacer tú con tu cuenta institucional.

---

## Opción A: abrir el proyecto ya armado

**Requisitos:** Power BI Desktop actualizado (el proyecto usa el formato PBIR). Si tu versión es antigua, actívalo en **Archivo → Opciones y configuración → Opciones → Características en versión preliminar** y marca *Formato de proyecto de Power BI (.pbip)* y *Almacenar informes con el formato de metadatos mejorado (PBIR)*. Luego reinicia Power BI.

1. Descarga la carpeta `powerbi/` completa. Los tres elementos deben quedar juntos:
   ```
   powerbi/
   ├── Practica_V_Complejas.pbip
   ├── Practica_V_Complejas.Report/
   └── Practica_V_Complejas.SemanticModel/
   ```
2. Haz doble clic en `Practica_V_Complejas.pbip` (o **Archivo → Abrir** y elígelo).
3. El proyecto no trae datos guardados, así que los visuales aparecen vacíos. Pulsa **Inicio → Actualizar**. Se cargan los 60 registros de la tabla `Logistica_Global`.
4. Haz doble clic en el cuadro de texto `Estudiante: [Apellido Nombre] | Fecha: [dd/mm/aaaa] | Nivel: [Nivel]` y escribe tus datos.
5. **Archivo → Guardar como**, elige el tipo **Archivo de Power BI (.pbix)** y usa el nombre que pide la guía:
   `Apellido_Nombre_Practica V_Complejas.pbix` (por ejemplo `Perez_Miguel_Practica V_Complejas.pbix`).
6. Revisa la lista de verificación del final y pasa al **Paso 5**.

Qué incluye el proyecto:

| Objeto | Configuración |
|---|---|
| Tabla `Logistica_Global` | 60 registros. `Ventas_USD` y `Costo_Envio_USD` son número entero y `Dias_Entrega` número decimal. Tiene además una columna oculta `Mes_Num` para que los meses salgan en orden cronológico (Enero → Junio) y no alfabético. |
| Gráfico de dispersión | Eje X = `Costo_Envio_USD`, Eje Y = `Dias_Entrega`, Valores = `ID_Pedido`, Leyenda = `Tipo_Envio`, Tamaño = `Ventas_USD`, con línea de tendencia activada. |
| Gráfico de líneas y columnas agrupadas | Eje X = `Región`, Eje Y de columna = **Promedio** de `Costo_Envio_USD`, Eje Y de línea = **Promedio** de `Dias_Entrega` (eje secundario), con etiquetas de datos. |
| Segmentaciones | `Mes` (lista desplegable) y `Tipo_Envio` (lista). |
| Tarjetas | Suma de `Ventas_USD` y promedio de `Dias_Entrega`. Cada una muestra su nombre una sola vez, como título, para no repetir texto. |
| Cuadros de texto | Título del dashboard, datos del estudiante y párrafo de análisis crítico. |

> Si al abrir el `.pbip` Power BI muestra un error, usa la **Opción B**. Con el Excel de `datos/` la tienes lista en unos 20 minutos.

---

## Opción B: construir el dashboard desde cero

### Paso 1: ingesta y validación técnica

1. Abre Power BI Desktop → **Inicio → Especificar datos**.
2. Abre `datos/Logistica_Global.xlsx`, selecciona las 61 filas (encabezado + 60 registros, de A1 a G61), cópialas con **Ctrl+C** y pégalas en la ventana *Especificar datos* con **Ctrl+V**. Si la primera fila no quedó como encabezado, usa *Usar la primera fila como encabezado*.
3. En **Nombre** escribe `Logistica_Global` → **Cargar**.
4. Ve a la **Vista de tabla** (icono de cuadrícula, a la izquierda):
   - Selecciona `Ventas_USD` → **Herramientas de columnas → Tipo de datos → Número entero**.
   - Haz lo mismo con `Costo_Envio_USD`.
   - Selecciona `Dias_Entrega` → **Número decimal**.
   - Verifica que `Dias_Entrega` muestre valores como `5.4` y no `54`. Si salen mal, tu configuración regional usa coma decimal: ve a **Archivo → Opciones → Archivo actual → Configuración regional**, elige *Inglés (Estados Unidos)* y vuelve a cargar los datos.
5. *(Opcional, recomendado)* Para que los meses salgan en orden cronológico:
   - **Herramientas de tabla → Nueva columna**:
     ```DAX
     Mes_Num = SWITCH([Mes], "Enero", 1, "Febrero", 2, "Marzo", 3, "Abril", 4, "Mayo", 5, "Junio", 6)
     ```
   - Selecciona la columna `Mes` → **Ordenar por columna → Mes_Num**.

### Paso 2: gráfico de dispersión

1. Vuelve a la **Vista de informe**. En *Visualizaciones* elige **Gráfico de dispersión**.
2. Arrastra los campos:
   - **Valores:** `ID_Pedido` (separa los 60 puntos)
   - **Eje X:** `Costo_Envio_USD`
   - **Eje Y:** `Dias_Entrega`
   - **Leyenda:** `Tipo_Envio`
   - **Tamaño:** `Ventas_USD`
3. Abre el panel **Análisis** (icono de lupa en *Visualizaciones*) → **Línea de tendencia → Activado**.
4. Observa la pendiente: es **negativa**, porque a mayor costo hay menos días de entrega (el Express es más rápido). Fíjate también en que dentro de cada nube los puntos más caros son los más lentos.

### Paso 3: gráfico mixto (eje dual por región)

1. Elige **Gráfico de líneas y de columnas agrupadas**.
2. Arrastra los campos:
   - **Eje X:** `Región`
   - **Eje Y de columna:** `Costo_Envio_USD`. Abre la flecha del campo dentro del panel y cambia **Suma → Promedio**.
   - **Eje Y de línea:** `Dias_Entrega` → también **Promedio**.
3. En **Formato → Visual → Etiquetas de datos → Activado**.
4. Deberías ver, de mayor a menor costo: Oeste $3,298 / 4.87 días · Sur $2,805 / 4.12 · Norte $2,195 / 3.67 · Este $1,972 / 3.28.

### Paso 4: ensamblaje e interactividad

1. Agrega una **Segmentación de datos** con `Mes` y otra con `Tipo_Envio`.
2. Agrega una **Tarjeta** con `Ventas_USD` (suma; debe mostrar **$1,035,700**) y otra con `Dias_Entrega` cambiada a **Promedio** (debe mostrar **4.02**).
3. **Insertar → Cuadro de texto** arriba, con el título: **Dashboard de Eficiencia de Red Distribuidora y Costos Logísticos**.
4. Agrega otro cuadro de texto con **nombre del estudiante, fecha y nivel**.
5. Agrega un cuadro de texto con el **párrafo de análisis crítico**. Puedes copiarlo de [`analisis/ANALISIS_CRITICO.md`](analisis/ANALISIS_CRITICO.md).
6. Diseño limpio, que es parte de la rúbrica:
   - Alinea los objetos con **Formato → Alinear** y **Distribuir horizontalmente**, y deja márgenes iguales.
   - Pon títulos cortos y propios en cada visual. En las tarjetas desactiva la *Etiqueta de categoría* y usa el título, o al revés, pero no las dos cosas.
   - Las etiquetas de datos del gráfico mixto permiten quitar las líneas de cuadrícula que sobren.

Distribución sugerida (lienzo de 1280 × 720):

```
┌───────────────────────────────────────────────────────────────┐
│     Dashboard de Eficiencia de Red Distribuidora y Costos ... │
│        Estudiante: ...   |   Fecha: ...   |   Nivel: ...      │
├──────────────┬──────────────┬───────────────┬─────────────────┤
│ Segm. Mes    │ Segm. Tipo   │ Tarjeta Ventas│ Tarjeta Días    │
├──────────────┴──────────────┴───┬───────────┴─────────────────┤
│                                 │                             │
│   Gráfico de dispersión         │   Gráfico mixto por región  │
│   (costo vs. días, tendencia)   │   (columnas + línea)        │
│                                 │                             │
├─────────────────────────────────┴─────────────────────────────┤
│  Análisis crítico (párrafo conclusivo)                        │
└───────────────────────────────────────────────────────────────┘
```

7. Guarda como `Apellido_Nombre_Practica V_Complejas.pbix`.

---

## Paso 5: presentación y publicación (lo haces tú con tu cuenta)

1. En Power BI Desktop, arriba a la derecha, **Iniciar sesión** con tu correo institucional.
2. Comprueba que el lienzo tenga tu **nombre, fecha y nivel** y que el archivo se llame `Apellido_Nombre_Practica V_Complejas.pbix`.
3. **Inicio → Publicar**.
4. Elige **Mi área de trabajo** → **Seleccionar**. Espera el mensaje *¡Listo!*.
5. Haz clic en *Abrir "…pbix" en Power BI* (o entra en <https://app.powerbi.com> → **Mi área de trabajo** → tu informe).
6. En el informe pulsa **Compartir**. En la configuración del vínculo elige quién puede verlo, normalmente *Personas de su organización* o las personas concretas que indique el docente, y luego **Copiar vínculo**.
7. Pega ese vínculo en la tarea del aula virtual.

> Si **Publicar** o **Compartir** aparecen desactivados, tu cuenta institucional no tiene licencia de Power BI (Pro / Fabric). Consulta al docente o a TI. Esto depende de la cuenta, no del archivo.

---

## Lista de verificación antes de entregar

- [ ] Tabla `Logistica_Global` con 60 filas; `Ventas_USD` y `Costo_Envio_USD` como número entero y `Dias_Entrega` como número decimal.
- [ ] Dispersión: X = costo, Y = días, Valores = ID_Pedido, Leyenda = Tipo_Envio, Tamaño = Ventas_USD, con línea de tendencia.
- [ ] Gráfico mixto con **Promedio** (no Suma) en las columnas y en la línea, y etiquetas de datos activadas.
- [ ] Segmentaciones de Mes y Tipo_Envio que filtran los demás visuales.
- [ ] Tarjeta con suma de ventas ($1,035,700) y tarjeta con promedio de días (4.02).
- [ ] Título arriba, nombre / fecha / nivel visibles y párrafo de análisis crítico.
- [ ] Objetos alineados y sin títulos repetidos.
- [ ] Archivo `Apellido_Nombre_Practica V_Complejas.pbix`, publicado en *Mi área de trabajo*, con el vínculo pegado en el aula virtual.
