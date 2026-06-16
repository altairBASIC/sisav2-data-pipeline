# Diccionario de Datos — SISAV2

Esquema canónico de las 36 columnas presentes en los exports Excel de SISAV2.
Cada fila describe una columna tal como aparece en los archivos fuente.

## Convenciones

- **Tipo**: `str`, `int`, `float`, `date`, `bool`.
- **Obligatoria**: `sí` si siempre debería tener valor; `no` si depende del instrumento/año.
- **Notas**: particularidades observadas (formatos inconsistentes, valores centinela, etc.).

## Esquema

| # | Columna | Tipo | Obligatoria | Descripción | Notas |
|---|---------|------|-------------|-------------|-------|
| 1 | `codigo_iniciativa` | str | sí | Identificador único de la iniciativa en SISAV2 | — |
| 2 | `nombre_iniciativa` | str | sí | Nombre descriptivo de la iniciativa | — |
| 3 | ... | ... | ... | ... | ... |

> **TODO**: Completar las 36 columnas a partir de los exports reales una vez disponibles.

## Columnas de linaje (añadidas por el pipeline)

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `_archivo_origen` | str | Nombre del archivo Excel fuente |
| `_convocatoria` | str | ID de convocatoria extraído del filename |
| `_fecha_proceso` | str | Timestamp ISO 8601 de la corrida del pipeline |
| `_version_pipeline` | str | Versión semántica del pipeline |
