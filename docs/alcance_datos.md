# Alcance de Datos - MVP

## Decisión de alcance

| Aspecto | Valor |
|---------|-------|
| **Formato procesado (MVP)** | Legacy - 36 columnas canónicas |
| **Archivos conformes** | 33 de 43 |
| **Filas consolidadas** | 1218 |
| **Período cubierto** | 2016–2025 (1S) + 1 convocatoria extensión 2027 |
| **Formato excluido** | Expandido - 41 a 63 columnas (formularios nuevos SISAV2) |
| **Archivos excluidos** | 10 |
| **Decisión** | El formato expandido queda fuera de este MVP, pendiente de definición con la contraparte (VcM) |

## Archivos procesados (formato legacy, 36 columnas)

Convocatorias históricas con esquema estable. Nombres de columnas idénticos
entre todos ellos: ver `src/schema.py` → `COLUMNAS_CANONICAS`.

## Archivos rechazados (formato expandido)

Los siguientes 10 archivos usan formularios SISAV2 más recientes con esquema
diferente. Se detectan automáticamente en la ingesta y se excluyen con
diagnóstico explícito.

### Lista de rechazados

| # | Archivo | Columnas | Período |
|---|---------|----------|---------|
| 1 | `POST_GRADO__conv49__...Entorno_Disciplinar_Profesional_2025_Po.xlsx` | 41 | 2025 |
| 2 | `PRE_GRADO__conv32__...Extensión_Académica_2025.xlsx` | 48 | 2025 |
| 3 | `PRE_GRADO__conv38__...Vinculación_con_Titulados_2025.xlsx` | 49 | 2025 |
| 4 | `PRE_GRADO__conv39__...Entorno_Disciplinar_Profesional_2025.xlsx` | 49 | 2025 |
| 5 | `PRE_GRADO__conv50__...Extensión_Académica_2025_2do_Semestre.xlsx` | 48 | 2025-2S |
| 6 | `PRE_GRADO__conv51__...Vinculación_con_Titulados_2025_2do_Semestre.xlsx` | 49 | 2025-2S |
| 7 | `PRE_GRADO__conv52__...Entorno_Disciplinar_Profesional_2025_2d.xlsx` | 49 | 2025-2S |
| 8 | `PRE_GRADO__conv71__...Entorno_Disciplinar_Profesional_-_1_Semestre_2.xlsx` | 63 | 2026-1S |
| 9 | `PRE_GRADO__conv72__...Extensión_Académica-_1_Semestre_2026.xlsx` | 55 | 2026-1S |
| 10 | `PRE_GRADO__conv73__...Vinculación_con_Titulados_as_-_1_Semestre_2026.xlsx` | 58 | 2026-1S |

### Diferencias de esquema detectadas

**Patrón común en el formato expandido (ejemplo: conv32, 48 columnas)**:

Columnas del canónico **ausentes** en el expandido (23):
- `N`, `Codigo`, `PLATAFORMA`, `UA`
- `Competencia Sello` → renombrada a `Competencia sello`
- `Competencia genérica` → renombrada a `Competencias génericas`
- `Contribución Interna/Externa` → renombrada a `Contribución interna/externa`
- `Nombre de la iniciativa` → renombrada a `Nombre de iniciativa`
- `Fecha Inicio/Termino` → renombrada a `Fecha de inicio/finalización`
- `Semestre Ejecución` → renombrada a `Semestre de ejecución de la iniciativa`
- `Cantidad Act Planificadas` → renombrada a `Cantidad de actividades planificadas`
- `Evidencia` → renombrada a `Existe de evidencia` / `Existe informe de evidencia`
- Columnas 100% vacías del legacy (`Dimensión`, `N estudiantes`, `N Docentes`, `N Titulados`, `Total`, `UA`, `Comentarios`) directamente eliminadas

Columnas **nuevas** en el expandido (no presentes en canónico):
- Conteos desagregados por género: `N de estudiantes (M/F/Otro)`, `N de titulados (M/F/Otro)`, `N de académicos (M/F/Otro)`, `N de funcionarios (M/F/Otro)`, `N de personas relacionadas a instituciones externas (M/F/Otro)`
- `N total de participantes de la iniciativa`
- `Académico postulante` (nombre del docente)
- `Objetivo de la iniciativa` (texto largo)
- `Código cátedra asociada`, `Nombre de asignatura asociada`, `Semestre de la cátedra`, `N de estudiantes en cátedra asociada`
- `Ciclo` / `Ciclo del modelo educativo`
- `Línea de vinculación`, `Logros de aprendizaje`, `Tipo de actividad`
- `instituciones externas` / `Instituciones externas`

**Formato conv71–73 (2026-1S, 55–63 columnas)**: variante aún más expandida con
campos de justificación (`Justifica PDI`, `Justificación competencia sello`,
`Justificación de Dominio`), internacionalización, geolocalización (`Comuna RM`,
`País`), y campos de formulario (`Adjunta documento`, `Coffee`, `Requerimiento`).

### Observaciones para integración futura

1. La mayoría de las diferencias son **renombramientos** (e.g. `Competencia Sello` → `Competencia sello`). Un mapeo de columnas resolvería ~60% de las incompatibilidades.
2. Los conteos desagregados por género en el formato nuevo son un superset de las columnas vacías `N estudiantes`, `N Docentes`, `N Titulados` del formato legacy.
3. Integrar el formato expandido requerirá definir con la contraparte: (a) un esquema unificado; (b) qué columnas nuevas son relevantes para el dashboard; (c) cómo consolidar los conteos agregados vs desagregados.
4. La estructura del pipeline ya soporta esto: basta con extender `src/ingest.py` con una función de mapeo de esquemas.

---

## Nota sobre `_semestre` derivado del filename

El campo de linaje `_semestre` se extrae del nombre del archivo mediante regex.
Solo está disponible para convocatorias recientes que usan el formato
`Proyecto_VcM_{N}er_Semestre_{año}` (6 de 33 archivos conformes).

Para las 27 convocatorias restantes (formato `INICIATIVAS_{año}`,
`EXTENSION_{año}`, `UET_{año}`), el semestre no está codificado en el nombre
del archivo y queda como `None`. **No se imputa un valor inventado.**

Una posible fuente alternativa para recuperar el semestre en estos casos es la
columna interna `Semestre Ejecución` del propio Excel, que contiene el semestre
de ejecución declarado por el docente. Sin embargo, esa columna tiene alta
variabilidad (75 variantes textuales) y requiere la normalización R-005 antes
de poder usarse como fuente confiable. **Se evaluará en fase posterior** si,
tras aplicar R-005, es viable poblar `_semestre` desde `Semestre Ejecución`
para los archivos que no lo traen en el nombre.
