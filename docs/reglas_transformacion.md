# Reglas de Transformación - SISAV2 Data Pipeline

Catálogo de todas las reglas de limpieza aplicadas por el pipeline.
Cada regla tiene un ID estable que aparece en tres lugares:
1. Este documento (explicación y justificación).
2. `src/transform.py` (implementación).
3. Audit log de salida (trazabilidad por registro).

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
| **Justificacion** | Validado en notebook 05: los valores de 2022 son conceptualmente distintos de los dominios especificos que aparecen desde 2024. Mezclarlos produce un campo semanticamente incoherente. |
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
