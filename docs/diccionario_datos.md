# Diccionario de datos - Dashboard VcM

**Documento definitivo** para el equipo de visualizacion y la contraparte de
VcM. Describe el esquema final de los dos datasets del dashboard, su cobertura
real, y como usarlos. Reemplaza a los diccionarios parciales anteriores.

## Los dos datasets

Ambos comparten **exactamente las mismas 42 columnas, en el mismo orden**, y
tienen 826 filas (una por iniciativa). Son intercambiables para el dashboard.

| Dataset | Contenido | Uso |
|---------|-----------|-----|
| `dashboard_real` (CSV y Parquet) | Datos 100% reales de SISAV 2022-2025. Las columnas que la fuente no captura estan presentes pero vacias. | Unica fuente valida para cifras institucionales, reporteria y acreditacion. |
| `dashboard_sintetico` (CSV y Parquet) | Datos 100% ficticios, todas las columnas pobladas, estadisticamente calcado del real (vocabularios, proporciones y distribuciones reales; generacion reproducible con semilla fija). | SOLO demostracion del dashboard completo. Nunca para reporteria, informes ni acreditacion. |

La columna `_origen_dato` (`"real"` / `"sintetico"`) identifica cada dataset de
forma inequivoca; el dashboard puede mostrarla como procedencia en cada vista.

**Advertencia sobre el sintetico:** sus filas no corresponden a ninguna
iniciativa real (codigos `DEMO-...`, nombres genericos, combinaciones
aleatorias). Es verosimil en agregado y ficticio en el detalle.

## Convenciones

- **Tipos**: `str` (texto), `float` (numerico con decimales), `int` (entero),
  `bool` (verdadero/falso). Los numericos y booleanos admiten vacio (NaN)
  donde no hay dato.
- **Multivalor**: los campos marcados usan `; ` (punto y coma + espacio) como
  separador. Para obtener una lista: `valor.split("; ")`.
- **NaN**: significa que el dato **no existe en la fuente** para esa
  iniciativa o periodo. No es un error ni un cero. Los conteos nunca se
  rellenan con 0 por defecto: un 0 es un cero informado de verdad.
- El formato Parquet preserva los tipos (recomendado); el CSV es para consumo
  universal.

## Esquema (42 columnas)

### Identificacion y filtros

| Columna | Tipo | Multivalor | Descripcion |
|---------|------|-----------|-------------|
| codigo | str | No | Codigo SISAV de la iniciativa. Vacio en el instrumento CENTRALIZADAS (el formulario no lo trae); usar `nombre_iniciativa` como identificador de respaldo. |
| nombre_iniciativa | str | No | Nombre de la iniciativa. Siempre presente. En el sintetico es un nombre generico de demostracion. |
| facultad | str | No | Facultad responsable (FAE, FCCOT, FCJS, FCNMMA, FCSJ, FHTCS, FING). |
| carrera | str | No | Carrera asociada. Coherente con su facultad tambien en el sintetico. |
| instrumento | str | No | Instrumento de VcM (EXTENSION, VEDP, VT, FCR, UTG, CENTRALIZADAS). |
| anio | int | No | Anio de la convocatoria (2022 a 2025). |
| semestre | str | No | Semestre de ejecucion, normalizado a `1S` / `2S` / `Anual`. Filtro obligatorio. No confundir con el semestre de la catedra asociada, que es otro concepto. |
| modalidad | str | No | Modalidad de ejecucion, normalizada a `Presencial` / `Online` / `Hibrida`. Filtro obligatorio. |
| estado_sisav | str | No | Estado en SISAV. Vocabulario heterogeneo entre periodos (FINALIZADO / Finalizada / EJECUCION / NO EJECUTADA, etc.); para clasificar "realizada vs no realizada" comparar en minusculas y por contencion. |

### Participantes desagregados (conteos por iniciativa)

| Columna | Tipo | Multivalor | Descripcion |
|---------|------|-----------|-------------|
| n_estudiantes | float | No | Estudiantes participantes. En 2025 la fuente los reporta por sexo (M/F/Otro) y aqui vienen sumados. |
| n_academicos | float | No | Academicos/docentes participantes. No incluye funcionarios. |
| n_titulados | float | No | Titulados participantes. |
| n_empleadores | float | No | Emprendedores/empleadores participantes. **Vacia en el real: ninguna planilla fuente 2022-2025 captura este dato.** |
| n_organizaciones_osc | float | No | Organizaciones/instituciones del medio externo participantes (proxy de organizaciones de la sociedad civil). |

### Desglose por rol (charlista / expositor / asistente)

Nueve columnas float, todas con la misma semantica (cuantas personas u
organizaciones de esa categoria participaron en cada rol):

| Columna | Tipo | Multivalor | Descripcion |
|---------|------|-----------|-------------|
| n_titulados_charlista | float | No | Titulados que participaron como charlistas. |
| n_titulados_expositor | float | No | Titulados que participaron como expositores. |
| n_titulados_asistente | float | No | Titulados que participaron como asistentes. |
| n_empleadores_charlista | float | No | Empleadores como charlistas. |
| n_empleadores_expositor | float | No | Empleadores como expositores. |
| n_empleadores_asistente | float | No | Empleadores como asistentes. |
| n_organizaciones_osc_charlista | float | No | Organizaciones como charlistas. |
| n_organizaciones_osc_expositor | float | No | Organizaciones como expositoras. |
| n_organizaciones_osc_asistente | float | No | Organizaciones como asistentes. |

**Todas vacias en el real: la fuente no registra roles de participacion.** En
el sintetico el desglose suma exacto al total de su categoria.

### Competencias

| Columna | Tipo | Multivalor | Descripcion |
|---------|------|-----------|-------------|
| competencia_sello | str | Si (`; `) | Competencias sello institucionales declaradas. En 2022-2023 proviene del campo de sello institucional (unica competencia de ese formato). |
| sello_tecnologia | bool | No | Bandera derivada del texto de `competencia_sello`: declara sello tecnologico. Vacia solo donde no hay sello declarado. |
| sello_responsabilidad_social | bool | No | Idem, sello de responsabilidad social. |
| sello_sustentabilidad | bool | No | Idem, sello de sustentabilidad/sostenibilidad. |
| sello_genero | bool | No | Idem, sello de genero. |
| competencia_generica | str | Si (`; `) | Competencias genericas. No existen en el formato 2022-2023. |

### Dominios disciplinares

| Columna | Tipo | Multivalor | Descripcion |
|---------|------|-----------|-------------|
| dominios_disciplinares | str | Si (`; `) | Dominios disciplinares asociados a la iniciativa. Existen en la fuente solo desde 2024. Concepto distinto del "area generica" que la fuente usaba en 2022-2023 (no se mapean entre si). |

### Otros indicadores

| Columna | Tipo | Multivalor | Descripcion |
|---------|------|-----------|-------------|
| ciclo_estudio | int | No | Ciclo del modelo educativo (0/1/2/3). **Vacia en el real** (no incorporada desde la fuente en esta version). |
| internacionalizacion | bool | No | Si la iniciativa tiene componente internacional. **Vacia en el real: la fuente no lo captura.** |
| catedra_asignatura | str | No | Nombre de la catedra/asignatura asociada. Cobertura parcial (~57% desde 2024): no todos los instrumentos la traen. |
| comuna_rm | str | No | Comuna de la Region Metropolitana donde se ejecuta. **Vacia en el real: la fuente no lo captura.** En el sintetico son comunas reales de la RM. |
| evidencia | str | No | Si la iniciativa cuenta con evidencia de ejecucion (`SI` / `NO`). Normalizada: en 2022-2023 se deriva del estado de evidencia de la fuente (COMPLETO e INCOMPLETO cuentan como SI, SIN EVIDENCIA como NO); en 2024-2025 la fuente trae el campo SI/NO directo. Filtro obligatorio. |

### Actividades (base del KPI I19)

| Columna | Tipo | Multivalor | Descripcion |
|---------|------|-----------|-------------|
| cantidad_act_planificadas | float | No | Actividades planificadas. Existe en la fuente en todos los anios. |
| cantidad_act_ejecutadas | float | No | Actividades ejecutadas. **Solo 2022-2023**: la fuente dejo de capturarla desde 2024. El KPI I19 (ejecutadas/planificadas x 100) solo es calculable con datos reales para 2022-2023. |

### Tabla de incidencias

| Columna | Tipo | Multivalor | Descripcion |
|---------|------|-----------|-------------|
| requiere_revision | bool | No | `True` si la iniciativa requiere atencion: evidencia faltante (`NO` o vacia), sin codigo, o sin facultad. Siempre poblada, misma regla en ambos datasets. |
| motivo_revision | str | Si (`; `) | Razones legibles: `sin evidencia`, `sin codigo`, `sin facultad`, concatenadas si hay varias. Cadena vacia donde no hay incidencia. |

### Linaje

| Columna | Tipo | Multivalor | Descripcion |
|---------|------|-----------|-------------|
| _archivo_origen | str | No | Planilla fuente de la que proviene la fila (trazabilidad), o el identificador del generador sintetico. |
| _anio | int | No | Anio de linaje (igual a `anio`). |
| _origen_dato | str | No | `"real"` o `"sintetico"`. |

## Cobertura por anio en el dataset real

Porcentaje de iniciativas del anio con dato. En el **sintetico todas las
columnas estan pobladas al 100%** en todos los anios. Las filas marcadas con
`(ausente en fuente)` estan vacias en el real porque la planilla de origen no
captura ese dato.

| Columna | 2022 | 2023 | 2024 | 2025 |
|---------|------|------|------|------|
| codigo | 98.6 | 100 | 96.0 | 87.0 |
| nombre_iniciativa | 100 | 100 | 100 | 100 |
| facultad | 100 | 100 | 98.3 | 100 |
| carrera | 100 | 100 | 98.9 | 100 |
| instrumento | 100 | 100 | 100 | 100 |
| semestre | 100 | 100 | 98.9 | 100 |
| modalidad | 100 | 100 | 98.9 | 99.4 |
| estado_sisav | 100 | 100 | 98.3 | 87.0 |
| n_estudiantes | 0 | 0 | 98.9 | 99.1 |
| n_academicos | 0 | 0 | 98.3 | 99.4 |
| n_titulados | 0 | 0 | 97.2 | 99.1 |
| n_empleadores (ausente en fuente) | 0 | 0 | 0 | 0 |
| n_organizaciones_osc | 0 | 0 | 95.5 | 80.9 |
| roles: las 9 columnas `*_charlista/expositor/asistente` (ausentes en fuente) | 0 | 0 | 0 | 0 |
| competencia_sello (y las 4 banderas `sello_*`) | 93.2 | 98.1 | 98.9 | 99.4 |
| competencia_generica | 0 | 0 | 94.3 | 100 |
| dominios_disciplinares | 0 | 0 | 88.1 | 88.4 |
| ciclo_estudio (ausente en fuente) | 0 | 0 | 0 | 0 |
| internacionalizacion (ausente en fuente) | 0 | 0 | 0 | 0 |
| catedra_asignatura | 0 | 0 | 56.8 | 58.6 |
| comuna_rm (ausente en fuente) | 0 | 0 | 0 | 0 |
| evidencia | 97.3 | 98.7 | 96.0 | 100 |
| cantidad_act_planificadas | 98.6 | 96.2 | 97.7 | 98.3 |
| cantidad_act_ejecutadas | 78.4 | 89.8 | 0 | 0 |
| requiere_revision / motivo_revision | 100 | 100 | 100 | 100 |
| _archivo_origen / _anio / _origen_dato | 100 | 100 | 100 | 100 |

Los ceros de 2022-2023 en participantes, competencia generica y dominios no son
perdida de datos: ese formato de planilla no capturaba esos campos.

## Guia de uso para el equipo de visualizacion

### Que dataset usar para que

- **Cifras institucionales, reporteria, acreditacion**: solo `dashboard_real`.
- **Demostracion del dashboard completo** (vistas que dependen de columnas
  vacias en el real): `dashboard_sintetico`, siempre etiquetado como datos
  sinteticos/demostrativos en pantalla.
- Ambos son intercambiables tecnicamente (mismo esquema): un mismo dashboard
  puede apuntar a uno u otro sin cambiar codigo, mostrando `_origen_dato`.

### Filtros obligatorios

| Filtro | Columna | Valores | Cobertura real |
|--------|---------|---------|----------------|
| Instrumento | instrumento | EXTENSION, VEDP, VT, FCR, UTG, CENTRALIZADAS | 100% |
| Facultad | facultad | 7 siglas de facultad | 98-100% |
| Carrera | carrera | ~60 carreras | 99-100% |
| Semestre | semestre | 1S, 2S, Anual | 99-100% |
| Estado | estado_sisav | vocabulario heterogeneo (ver esquema) | 87-100% |
| Modalidad | modalidad | Presencial, Online, Hibrida | 99-100% |
| Evidencia | evidencia | SI, NO | 96-100% |

### Tabla de incidencias

Filtrar `requiere_revision == True` para obtener los casos que requieren
atencion; `motivo_revision` explica por que, en texto legible y multivalor
(`sin evidencia; sin codigo`). En el dataset real quedan marcadas 183 de 826
iniciativas (22.2%): 135 sin evidencia, 54 sin codigo (instrumento
CENTRALIZADAS) y 3 sin facultad. Donde `requiere_revision` es `False`,
`motivo_revision` es cadena vacia (no NaN).

### Advertencias de interpretacion

- **No sumar columnas de cobertura parcial esperando totales institucionales.**
  Los conteos de participantes son por iniciativa registrada, no un censo:
  una suma subestima el total real y mezcla iniciativas con y sin dato. Usar
  promedios/medianas por iniciativa, o totales acompanados de su cobertura.
- **Los huecos por anio son reales, no errores.** Un NaN refleja que el
  formulario de ese anio no capturaba el campo. No imputar ni interpolar.
- **No comparar conteos de participantes entre 2022-2023 y 2024-2025**: los
  anios viejos no tienen desagregacion, solo existia un total agregado de
  asistentes que no forma parte de este esquema.
- **Las banderas `sello_*` no son excluyentes**: una iniciativa puede declarar
  varios sellos, por eso las categorias no suman el total de iniciativas.
- Los campos float pueden traer NaN: usar operaciones que ignoren nulos
  (`dropna`, sumas con `min_count`), nunca rellenar con 0.

## Limitaciones de origen documentadas

1. **Columnas ausentes en la fuente en todo el periodo**: emprendedores/
   empleadores, los 9 desgloses por rol de participacion, comuna de ejecucion
   (RM), internacionalizacion y ciclo de estudio. Ningun formulario 2022-2025
   los captura. Para tenerlos con datos verdaderos, VcM debe incorporarlos al
   instrumento de registro; mientras tanto solo el sintetico puede demostrar
   esas vistas.
2. **Participantes desagregados solo desde 2024** (estudiantes, academicos,
   titulados, organizaciones). En 2022-2023 la fuente solo registraba un total
   agregado de asistentes.
3. **KPI I19 (ejecutadas/planificadas) solo calculable con datos reales para
   2022-2023**: la fuente dejo de capturar las actividades ejecutadas desde
   2024. Recuperar el KPI hacia adelante requiere volver a registrar ese campo.
4. **KPI de dominios disciplinares en su forma literal** ("% de los dominios
   del plan de estudios de cada carrera cubiertos por VcM") **no es calculable**:
   falta el catalogo oficial de dominios por carrera. Lo medible hoy es la
   declaracion de dominios en las iniciativas (~88% desde 2024). Si VcM entrega
   el catalogo, el calculo literal es directo sobre la columna existente.
5. **El instrumento CENTRALIZADAS no trae codigo ni estado**, por eso esas
   columnas bajan a ~87-96% en 2024-2025; usar `nombre_iniciativa` como
   identificador de respaldo.
6. **Catedra/asignatura con cobertura parcial (~57%)**: no todos los
   instrumentos la registran.
7. **Una planilla fuente sin anio determinable** (61 iniciativas centralizadas)
   quedo excluida de ambos datasets para no inventarle un periodo; puede
   reincorporarse si VcM confirma su anio.

## Normalizaciones aplicadas

Los valores llegan normalizados desde el proceso de extraccion y limpieza; el
detalle regla por regla (IDs R-001 en adelante) esta en el documento de reglas
de transformacion. Las mas relevantes para el consumo:

- Separador multivalor unificado a `; ` en competencias y dominios, sin
  fragmentar frases que contienen comas internas.
- `evidencia` unificada a SI/NO desde tres formatos de origen distintos.
- `modalidad` y `semestre` llevados a vocabularios controlados
  (Presencial/Online/Hibrida; 1S/2S/Anual).
- Conteos con celdas sucias (por ejemplo `2; 3`) resueltos tomando el primer
  numero.
- Archivos fuente duplicados (copias con nombre corrupto o sufijo de copia)
  deduplicados antes de consolidar; el universo son las iniciativas reales
  (filas con identificador), no las filas de plantilla vacias.
- Incidencias (`requiere_revision` / `motivo_revision`) calculadas con la misma
  regla en ambos datasets.
