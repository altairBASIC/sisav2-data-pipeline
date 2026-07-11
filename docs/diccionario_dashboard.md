# Diccionario del Dashboard VcM

Referencia para el equipo de visualizacion. Describe las dos tablas limpias
generadas por `notebooks/07_extraccion_final.ipynb` a partir de las planillas
fuente de SISAV2, siguiendo el diagnostico de viabilidad de
`notebooks/06_viabilidad_columnas.ipynb`.

**Por que dos tablas y no una:** la disponibilidad de datos cambia fuerte por
periodo. Los participantes desagregados (estudiantes, academicos, titulados)
solo existen desde 2024. Meter todo en una sola tabla obligaria a dejar 2022-2023
llenos de huecos y a prometer una desagregacion que esos anios no tienen. Se
separan para no mentir por omision.

- **Tabla A (`dashboard_participantes_2024_2025`)**: dataset rico, solo 2024-2025.
  Usar para metricas de participantes.
- **Tabla B (`dashboard_historico_2022_2025`)**: serie comparable 2022-2025.
  Usar para evolucion del numero de iniciativas y su distribucion.

---

## Tabla A - dashboard_participantes_2024_2025

Una fila por iniciativa. Solo anios 2024 y 2025 (los unicos con participantes
desagregados). Fuente: `data/clean/dashboard_participantes_2024_2025.{csv,parquet}`.

| Columna | Tipo | Multivalor | Separador | Desde | Descripcion |
|---------|------|-----------|-----------|-------|-------------|
| codigo | str | No | - | 2024 | Codigo SISAV de la iniciativa. Vacio (NaN) en el instrumento CENTRALIZADAS, que no trae codigo; usar `nombre_iniciativa` como identificador en ese caso. |
| nombre_iniciativa | str | No | - | 2024 | Nombre de la iniciativa. Siempre presente; identificador de respaldo. |
| facultad | str | No | - | 2024 | Facultad responsable. |
| carrera | str | No | - | 2024 | Carrera asociada. |
| instrumento | str | No | - | 2024 | Instrumento de VcM derivado del archivo fuente (EXTENSION, VEDP, VT, UTG, CENTRALIZADAS). |
| anio | int | No | - | 2024 | Anio de la convocatoria. |
| estado_sisav | str | No | - | 2024 | Estado en SISAV. Vacio en CENTRALIZADAS 2025 (el formulario no incluye la columna). |
| n_estudiantes | float | No | - | 2024 | Numero de estudiantes participantes. En 2025 suma los conteos por sexo (M/F/Otro). NaN si no hay dato. |
| n_academicos_docentes | float | No | - | 2024 | Numero de academicos/docentes participantes. En 2025 suma M/F/Otro. No incluye funcionarios. NaN si no hay dato. |
| n_titulados | float | No | - | 2024 | Numero de titulados participantes. En 2025 suma M/F/Otro. NaN si no hay dato. |
| n_organizaciones_osc | float | No | - | 2024 | Numero de organizaciones/instituciones del medio externo participantes. Proxy de organizaciones de la sociedad civil. NaN si no hay dato. |
| competencia_sello | str | Si | `; ` | 2024 | Competencias sello institucionales asociadas. |
| competencia_generica | str | Si | `; ` | 2024 | Competencias genericas asociadas. |
| dominios_disciplinares | str | Si | `; ` | 2024 | Dominios disciplinares asociados (base del KPI 1). Cobertura ~88%. Concepto distinto del area generica 2022-2023; separadores de origen normalizados a `; `, sin dividir por coma simple (las frases tienen comas internas). `No aplica` = sin dato. |
| catedra_asignatura | str | No | - | 2024 | Nombre de la catedra/asignatura asociada. Cobertura PARCIAL (~57%): en 2024 solo el instrumento VEDP la trae; en 2025 la traen 3 de 4 instrumentos. NaN donde no existe. |
| cantidad_act_planificadas | float | No | - | 2024 | Actividades planificadas (97-98%). Celdas sucias tipo `2; 3` se resuelven con el primer numero. |
| cantidad_act_ejecutadas | float | No | - | - | Vacia en esta tabla: la fuente 2024-2025 no captura ejecutadas. Presente por consistencia de esquema; el dato real vive en la tabla historica (2022-2023). |
| evidencia | str | No | - | 2024 | Si la iniciativa cuenta con evidencia (SI/NO, campo directo de la fuente 2024-2025). |
| _archivo_origen | str | No | - | 2024 | Archivo fuente (trazabilidad). |
| _anio | int | No | - | 2024 | Anio derivado del archivo fuente (linaje; igual a `anio`). |

### Cobertura Tabla A (% poblado por anio)

| Columna | 2024 | 2025 |
|---------|------|------|
| n_estudiantes | 98.9 | 99.1 |
| n_academicos_docentes | 98.3 | 99.4 |
| n_titulados | 97.2 | 99.1 |
| n_organizaciones_osc | 95.5 | 80.9 |
| competencia_sello | 98.9 | 99.4 |
| competencia_generica | 94.3 | 100.0 |
| dominios_disciplinares | 88.1 | 88.4 |
| catedra_asignatura | 56.8 | 58.6 |
| cantidad_act_planificadas | 97.7 | 98.3 |
| cantidad_act_ejecutadas | 0.0 | 0.0 |
| evidencia | 96.0 | 100.0 |
| codigo | 96.0 | 87.0 |
| estado_sisav | 98.3 | 87.0 |

---

## Tabla B - dashboard_historico_2022_2025

Una fila por iniciativa. Todos los anios 2022-2025, solo columnas comparables en
todo el periodo. Fuente: `data/clean/dashboard_historico_2022_2025.{csv,parquet}`.

| Columna | Tipo | Multivalor | Separador | Desde | Descripcion |
|---------|------|-----------|-----------|-------|-------------|
| codigo | str | No | - | 2022 | Codigo SISAV de la iniciativa. Vacio en CENTRALIZADAS. |
| nombre_iniciativa | str | No | - | 2022 | Nombre de la iniciativa. Identificador de respaldo. |
| facultad | str | No | - | 2022 | Facultad responsable. |
| carrera | str | No | - | 2022 | Carrera asociada. |
| instrumento | str | No | - | 2022 | Instrumento de VcM derivado del archivo fuente. |
| anio | int | No | - | 2022 | Anio de la convocatoria. |
| estado_sisav | str | No | - | 2022 | Estado en SISAV. |
| competencia_sello | str | Si | `; ` | 2022 | Competencias sello. En 2022-2023 proviene del campo `Sello Institucional` (unica competencia registrada en ese formato; no hay competencia generica). |
| total_participantes | float | No | - | 2022 | Total agregado de personas por iniciativa. En 2022-2023 es `Total Asistentes`; en 2024-2025 es el total agregado de participantes. Es un headcount agregado, NO una desagregacion. Cobertura baja en 2022 (~67%). NaN si no hay dato. |
| cantidad_act_planificadas | float | No | - | 2022 | Actividades planificadas (96-99% en todos los anios). |
| cantidad_act_ejecutadas | float | No | - | 2022 | Actividades ejecutadas, SOLO 2022-2023 (78-90%; la fuente dejo de capturarla desde 2024). Base del KPI I19 real. |
| evidencia | str | No | - | 2022 | Si la iniciativa cuenta con evidencia (SI/NO). En 2022-2023 derivada de `Estado de Evidencia` (COMPLETO/INCOMPLETO -> SI, SIN EVIDENCIA -> NO); en 2024-2025 campo directo. |
| _archivo_origen | str | No | - | 2022 | Archivo fuente (trazabilidad). |
| _anio | int | No | - | 2022 | Anio derivado del archivo fuente (linaje; igual a `anio`). |

### Cobertura Tabla B (% poblado por anio)

| Columna | 2022 | 2023 | 2024 | 2025 |
|---------|------|------|------|------|
| competencia_sello | 93.2 | 98.1 | 98.9 | 99.4 |
| total_participantes | 66.9 | 90.4 | 97.7 | 99.4 |
| estado_sisav | 100.0 | 100.0 | 98.3 | 87.0 |
| codigo | 98.6 | 100.0 | 96.0 | 87.0 |
| cantidad_act_planificadas | 98.6 | 96.2 | 97.7 | 98.3 |
| cantidad_act_ejecutadas | 78.4 | 89.8 | 0.0 | 0.0 |
| evidencia | 97.3 | 98.7 | 96.0 | 100.0 |

---

## Que tabla usar para que grafico

| Necesito graficar... | Tabla | Notas |
|----------------------|-------|-------|
| Participantes por tipo (estudiantes, academicos, titulados) | A | Solo 2024-2025. |
| Organizaciones del medio externo participantes | A | Solo 2024-2025. |
| Competencias sello y genericas | A | Genericas solo desde 2024. |
| Catedra/asignatura asociada | A | Atributo opcional, cobertura parcial. |
| Numero de iniciativas por anio (evolucion) | B | Serie completa 2022-2025. |
| Distribucion de iniciativas por facultad / instrumento / estado | B | Serie completa 2022-2025. |
| Evolucion de competencia sello en el tiempo | B | Serie completa 2022-2025. |
| Total de asistentes/participantes por anio | B | Es agregado; ver advertencia abajo. |

## Notas para consumo

- **Separador multivalor**: los campos marcados como multivalor usan `; `. Para
  obtener una lista: `valor.split("; ")`.
- **NaN**: significa que el dato no existe en la fuente para ese periodo o esa
  iniciativa. No es un error ni un cero; refleja la evolucion del formulario de
  VcM. Los conteos nunca se rellenan con 0 por defecto.
- **Tipos numericos**: las columnas float pueden tener NaN. Usar `dropna()` antes
  de operar.

## Advertencias explicitas

- **No sumar las columnas de participantes de la Tabla A esperando totales
  institucionales.** La cobertura es *por iniciativa registrada*, no es un censo.
  Sumar `n_estudiantes` (u otras) mezcla iniciativas con y sin dato y subestima el
  total real. Usar promedios o medianas por iniciativa, o totales acompanados de
  su cobertura declarada, nunca como cifra institucional cerrada.
- **`total_participantes` (Tabla B) no es comparable columna a columna con la
  suma de la Tabla A.** En 2022-2023 mide asistentes (agregado, sin desglose); en
  2024-2025 mide participantes totales. Sirve para tendencia, no para conciliar
  cifras exactas entre periodos.
- **Emprendedores / empleadores participantes: NO disponible.** El diagnostico
  confirmo que ninguna fuente (2022 a 2025) tiene una columna de conteo de
  emprendedores o empleadores. No se incluye ni se aproxima. Si el dashboard lo
  requiere, debe levantarse con la contraparte de VcM porque el dato no se captura
  en el instrumento.
- **Archivo excluido:** `Plantilla Iniciativas Centralizadas.xlsm` (61
  iniciativas) no trae anio en el nombre ni fechas parseables, por lo que no se
  pudo asignar a un periodo y quedo fuera de ambas tablas (mismo criterio que el
  diagnostico). Si se confirma su anio con VcM, puede reincorporarse.

## Archivos de salida

- `data/clean/dashboard_participantes_2024_2025.csv` / `.parquet`
- `data/clean/dashboard_historico_2022_2025.csv` / `.parquet`

El `.parquet` preserva tipos (recomendado para pandas/polars); el `.csv` es para
consumo universal. Ambos archivos de datos viven en `data/clean/`, que esta
gitignoreado por contener datos reales de VcM.
