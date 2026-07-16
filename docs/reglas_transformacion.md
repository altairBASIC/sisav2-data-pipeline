# Reglas de Transformación - SISAV2 Data Pipeline

Catalogo de todas las reglas de limpieza aplicadas por el pipeline.
Cada regla tiene un ID estable que aparece en tres lugares:
1. Este documento (explicacion y justificacion).
2. La implementacion del proceso de limpieza correspondiente.
3. Audit log de salida (trazabilidad por registro), donde aplica.

> **Nota sobre numeracion**: los IDs son estables, no contiguos y nunca se
> reusan. R-006, R-007 y R-008 fueron evaluadas durante el diseño y descartadas
> (documentadas abajo). El hueco entre R-005 y R-009 es intencional: renumerar
> romperia la trazabilidad con audit logs ya generados.

## Estructura de cada regla

| Campo | Descripción |
|-------|-------------|
| **ID** | Identificador estable `R-XXX` |
| **Nombre** | Nombre corto descriptivo |
| **Columnas afectadas** | Lista de columnas sobre las que opera |
| **Descripción** | Qué hace la regla |
| **Justificación** | Por qué se aplica |
| **Tipo** | `normalización`, `imputación`, `descarte`, `corrección` |
| **Estado** | `aprobada`, `pendiente`, `descartada` |

---

## Reglas implementadas

### R-001 - Normalización de espacios en blanco

| Campo | Valor |
|-------|-------|
| **ID** | R-001 |
| **Nombre** | Normalización de espacios |
| **Columnas afectadas** | Todas las columnas de tipo `str` (excepto N, Monto, fechas) |
| **Descripción** | Elimina espacios iniciales/finales y colapsa espacios múltiples internos a uno solo |
| **Justificación** | 290+ valores con padding detectados en perfilado (Grupo de interés, Nombre de la iniciativa, Competencia genérica, Perfil del entorno, Semestre Ejecución) |
| **Tipo** | normalización |
| **Estado** | implementada |

---

### R-002 - Reemplazo de tabs y newlines internos

| Campo | Valor |
|-------|-------|
| **ID** | R-002 |
| **Nombre** | Reemplazo de caracteres de control |
| **Columnas afectadas** | Todas las columnas de tipo `str` |
| **Descripción** | Reemplaza `\t` y `\n` internos por espacio simple |
| **Justificación** | 186 valores en Competencia genérica contienen tabs literales; algunos campos tienen saltos de línea embebidos |
| **Tipo** | normalización |
| **Estado** | implementada |

---

### R-003 - Eliminación de puntos finales en campos multivalor

| Campo | Valor |
|-------|-------|
| **ID** | R-003 |
| **Nombre** | Strip de puntos en multivalor |
| **Columnas afectadas** | ODS, Competencia Sello, Área de influencia, Competencia genérica, PDI |
| **Descripción** | Elimina el `.` final de cada ítem individual en campos separados por `"; "` o `" / "`, sin concatenar ni reordenar ítems |
| **Justificación** | Artefacto del formulario SISAV2: cada opción se almacena con punto final (e.g. `"Educación de calidad.; Alianzas."` → `"Educación de calidad; Alianzas"`) |
| **Tipo** | normalización |
| **Estado** | implementada |

---

### R-004 - Conversión de fechas a datetime

| Campo | Valor |
|-------|-------|
| **ID** | R-004 |
| **Nombre** | Parsing de fechas |
| **Columnas afectadas** | Fecha Inicio, Fecha Termino |
| **Descripción** | Convierte string `DD/MM/YYYY` a tipo `datetime64`. Valores no parseables quedan como `NaT` y se registran en el audit log |
| **Justificación** | Actualmente son strings; impide cálculos de duración, filtros temporales y ordenamiento |
| **Tipo** | normalización |
| **Estado** | implementada |

---

### R-005 - Normalización de Semestre Ejecución

| Campo | Valor |
|-------|-------|
| **ID** | R-005 |
| **Nombre** | Vocabulario controlado de semestre |
| **Columnas afectadas** | Semestre Ejecución |
| **Descripción** | Normaliza a vocabulario controlado: `1S`, `2S`, `Anual`, `Otro`. Valores que caen en `Otro` se registran en el audit log con su valor original |
| **Justificación** | 75 variantes textuales para ~3 categorías conceptuales; el 82% (Primer/Segundo Semestre + Anual) se mapea directo |
| **Tipo** | normalización |
| **Estado** | implementada |

---

### R-009 - Punto final en nombres de iniciativa

| Campo | Valor |
|-------|-------|
| **ID** | R-009 |
| **Nombre** | Strip de punto final en títulos |
| **Columnas afectadas** | Nombre de la iniciativa |
| **Descripción** | Elimina `.` final en nombres de iniciativa de menos de 100 caracteres |
| **Justificación** | 59 nombres terminan en `.` innecesario (son títulos, no oraciones) |
| **Tipo** | normalización |
| **Estado** | implementada |

---

## Reglas del consolidado de indicadores

### R-010 - Separacion de Area generica y dominios disciplinares

| Campo | Valor |
|-------|-------|
| **ID** | R-010 |
| **Nombre** | Separacion area/dominios |
| **Columnas afectadas** | dominios_disciplinares, area_generica (nueva) |
| **Descripcion** | En planillas 2022-2023 (Familia A), la columna "Area" contiene categorias genericas de VcM (RELACION_CON_EL_ENTORNO, EXTENSION, TITULADOS, DIFUSION_Y_DIVULGACION_DE_LA_INVESTIGACION), no dominios disciplinares. Se mapea a `area_generica` en vez de `dominios_disciplinares`. Dominios queda en NaN para 2022-2023. |
| **Justificacion** | Validado en la exploracion de las planillas origen: los valores de 2022 son conceptualmente distintos de los dominios especificos que aparecen desde 2024. Mezclarlos produce un campo semanticamente incoherente. |
| **Tipo** | correccion de mapeo |
| **Estado** | implementada |

---

### R-011 - Limpieza de artefacto vscode-resource

| Campo | Valor |
|-------|-------|
| **ID** | R-011 |
| **Nombre** | Eliminar patron de renderizado incrustado |
| **Columnas afectadas** | dominios_disciplinares |
| **Descripcion** | Elimina el patron `[/](https://file+.vscode-resource.vscode-cdn.net/)` que puede colarse como separador en campos multivalor al copiar desde VS Code. Se reemplaza por `; `. |
| **Justificacion** | Artefacto de renderizado, no dato real. |
| **Tipo** | normalizacion |
| **Estado** | implementada |

---

### R-012 - Unificacion de separadores multivalor

| Campo | Valor |
|-------|-------|
| **ID** | R-012 |
| **Nombre** | Normalizar separador a punto y coma |
| **Columnas afectadas** | dominios_disciplinares, area_generica, competencia_sello, ods |
| **Descripcion** | Unifica separadores inconsistentes (coma `,`, punto y coma `;`, variantes con/sin espacio) al estandar `; ` (punto y coma + espacio). Aplica strip a cada item y elimina items vacios. |
| **Justificacion** | Las distintas familias de formato usan separadores distintos. Un separador unico permite split confiable en visualizacion. |
| **Tipo** | normalizacion |
| **Estado** | implementada |

---

### R-013 - Unificacion del separador / a ;  en multivalor

| Campo | Valor |
|-------|-------|
| **ID** | R-013 |
| **Nombre** | Normalizar separador barra con espacios |
| **Columnas afectadas** | dominios_disciplinares, area_generica, competencia_sello, ods |
| **Descripcion** | Reemplaza el patron ` / ` (espacio-barra-espacio) por `; ` en campos multivalor. No toca barras sin espacios (como "y/o" o fechas) que son parte del texto. Tras el reemplazo, re-aplica strip de items y elimina items vacios. |
| **Justificacion** | Algunos archivos fuente (especialmente VEDP 2024) usan ` / ` como separador entre dominios disciplinares. Unificarlo a `; ` garantiza un split confiable para el equipo de visualizacion. |
| **Tipo** | normalizacion |
| **Estado** | implementada |

---

## Reglas de la capa dashboard (datasets real y sintetico)

Reglas aplicadas al construir los datasets `dashboard_real` y
`dashboard_sintetico` (esquema unificado de 42 columnas). Documentadas en el
diccionario de datos definitivo; aqui se catalogan con ID estable.

### R-014 - Deduplicacion de archivos fuente redundantes

| Campo | Valor |
|-------|-------|
| **ID** | R-014 |
| **Columnas afectadas** | Todas (nivel archivo) |
| **Descripcion** | Excluye copias redundantes de planillas fuente: nombres con codificacion corrupta (mojibake) o sufijo de copia `(n)`. Se conserva el archivo de nombre limpio. |
| **Justificacion** | Evitar contar dos veces las mismas iniciativas de 2025. |
| **Tipo** | descarte |
| **Estado** | implementada |

### R-015 - Universo de iniciativas reales

| Campo | Valor |
|-------|-------|
| **ID** | R-015 |
| **Columnas afectadas** | Todas (nivel fila) |
| **Descripcion** | Solo se consideran filas con identificador poblado (codigo o nombre de iniciativa). Las filas de plantilla vacias se excluyen. Un archivo sin anio determinable (61 iniciativas centralizadas) se excluye completo para no inventarle periodo. |
| **Justificacion** | Las plantillas traen filas vacias que arrastrarian la cobertura hacia abajo de forma artificial. |
| **Tipo** | descarte |
| **Estado** | implementada |

### R-016 - Normalizacion multivalor por tipo de campo

| Campo | Valor |
|-------|-------|
| **ID** | R-016 |
| **Columnas afectadas** | competencia_sello, competencia_generica, dominios_disciplinares |
| **Descripcion** | Unifica el separador a `; ` con estrategia por tipo de campo: etiquetas cortas se dividen por `;` y `,`; frases largas respetan comillas y comas internas (no se dividen por coma simple); dominios ademas dividen por el patron `., ` del formato 2024 y tratan `No aplica` como sin dato. |
| **Justificacion** | Los separadores de origen varian por anio y campo; dividir frases por coma simple las fragmentaria. Extiende R-012/R-013 a la capa dashboard. |
| **Tipo** | normalizacion |
| **Estado** | implementada |

### R-017 - Evidencia a SI/NO

| Campo | Valor |
|-------|-------|
| **ID** | R-017 |
| **Columnas afectadas** | evidencia |
| **Descripcion** | Unifica tres formatos de origen a SI/NO: el estado de evidencia 2022-2023 (COMPLETO e INCOMPLETO -> SI, SIN EVIDENCIA -> NO, incluyendo variantes sucias), y los campos SI/NO y Si/No directos de 2024 y 2025. |
| **Justificacion** | Filtro obligatorio del dashboard; INCOMPLETO cuenta como SI porque existe evidencia aunque incompleta. |
| **Tipo** | normalizacion |
| **Estado** | implementada |

### R-018 - Modalidad a vocabulario controlado

| Campo | Valor |
|-------|-------|
| **ID** | R-018 |
| **Columnas afectadas** | modalidad |
| **Descripcion** | Normaliza variantes de origen (PRESENCIAL/ONLINE/HIBRIDO vs Presencial/Online/Hibrida) a `Presencial` / `Online` / `Hibrida`. |
| **Justificacion** | Filtro obligatorio; sin normalizar, un mismo valor apareceria como categorias distintas segun el anio. |
| **Tipo** | normalizacion |
| **Estado** | implementada |

### R-019 - Semestre de ejecucion a 1S/2S/Anual

| Campo | Valor |
|-------|-------|
| **ID** | R-019 |
| **Columnas afectadas** | semestre |
| **Descripcion** | Normaliza PRIMERO/`Primer semestre` -> `1S`, SEGUNDO/`Segundo semestre` -> `2S`, ANUAL -> `Anual`. Excluye explicitamente el semestre de la catedra asociada, que es otro concepto. Extiende R-005 a la capa dashboard. |
| **Justificacion** | Filtro obligatorio y nivel micro de los graficos. |
| **Tipo** | normalizacion |
| **Estado** | implementada |

### R-020 - Primer numero en conteos sucios

| Campo | Valor |
|-------|-------|
| **ID** | R-020 |
| **Columnas afectadas** | cantidad_act_planificadas, cantidad_act_ejecutadas |
| **Descripcion** | En celdas con mas de un valor (por ejemplo `2; 3`) se toma el primer numero que aparece. |
| **Justificacion** | Perder la celda completa por un separador espurio seria peor que la aproximacion; casos poco frecuentes. |
| **Tipo** | correccion |
| **Estado** | implementada |

### R-021 - Marcado de incidencias

| Campo | Valor |
|-------|-------|
| **ID** | R-021 |
| **Columnas afectadas** | requiere_revision, motivo_revision (nuevas) |
| **Descripcion** | Marca `requiere_revision = True` cuando la iniciativa tiene evidencia faltante (NO o vacia), no tiene codigo, o no tiene facultad; `motivo_revision` concatena las razones con `; ` y queda vacia donde no hay incidencia. Misma regla en ambos datasets. |
| **Justificacion** | Tabla de incidencias solicitada para derivar casos al equipo de Front-End. |
| **Tipo** | correccion |
| **Estado** | implementada |

---

## Reglas descartadas

### R-006 - ~~Monto = 0 → NaN~~ (DESCARTADA)

| Campo | Valor |
|-------|-------|
| **ID** | R-006 |
| **Nombre** | Anulación de montos cero |
| **Columnas afectadas** | Monto |
| **Descripción** | Convertiría `0` a `NaN` |
| **Justificación del descarte** | `$0` puede significar legítimamente "iniciativa sin financiamiento asignado", información distinta de "no informado". Convertirlo a `NaN` destruiría esa distinción semántica y alteraría los totales de monto. **Decisión pendiente de confirmar con la contraparte (VcM)**. |
| **Tipo** | imputación |
| **Estado** | descartada |

---

### R-007 - ~~Eliminación de columnas 100% vacías~~ (DESCARTADA)

| Campo | Valor |
|-------|-------|
| **ID** | R-007 |
| **Nombre** | Drop de columnas vacías |
| **Columnas afectadas** | UA, Área, Dimensión, Modalidad, N estudiantes, N Docentes, N Titulados, N Instituciones del medio externo participantes, Total, Comentarios |
| **Descripción** | Eliminaría las 10 columnas sin ningún valor en el lote legacy |
| **Justificación del descarte** | Estas columnas (especialmente los conteos: N estudiantes, N Docentes, N Titulados, Total) **vienen pobladas en el formato expandido** (2025-2S, 2026-1S) con conteos desagregados por género. Son indicadores relevantes para acreditación. Eliminarlas rompería el esquema canónico al incorporar datos nuevos. Se conservan marcadas como vacías en este lote. |
| **Tipo** | descarte |
| **Estado** | descartada |

---

### R-008 - ~~Eliminación de columna PLATAFORMA~~ (DESCARTADA)

| Campo | Valor |
|-------|-------|
| **ID** | R-008 |
| **Nombre** | Drop de columna invariante |
| **Columnas afectadas** | PLATAFORMA |
| **Descripción** | Eliminaría la columna que solo contiene `"SISAV2"` |
| **Justificación del descarte** | Aunque invariante en el lote actual, conservar `PLATAFORMA` mantiene la integridad del esquema canónico de 36 columnas y es consistente con la decisión de no eliminar columnas vacías (R-007). Si en el futuro se ingestan datos de otra plataforma, la columna ya existirá. |
| **Tipo** | descarte |
| **Estado** | descartada |
