# Esquema unificado del dashboard VcM (real y sintetico)

Referencia de los dos datasets intercambiables generados por
`notebooks/08_datasets_dashboard.ipynb`. Ambos tienen **exactamente las mismas
39 columnas, en el mismo orden** (el notebook lo verifica con un `assert`):

| Dataset | Ubicacion | Contenido |
|---------|-----------|-----------|
| Real | `data/clean/dashboard_real.{csv,parquet}` | Datos 100% reales de SISAV2 (2022-2025). Las columnas que la fuente no captura estan presentes pero vacias (NaN). |
| Sintetico | `data/synthetic/dashboard_sintetico.{csv,parquet}` | Datos 100% ficticios, todas las columnas pobladas, estadisticamente calcado del real (seed fijo 42). |

La columna `_origen_dato` (`"real"` / `"sintetico"`) identifica cada archivo de
forma inequivoca. El real vive en `data/clean/` (confidencial, gitignoreado); el
sintetico en `data/synthetic/` (ficticio, versionable). Nunca mezclados.

## ADVERTENCIA sobre el dataset sintetico

**El sintetico es SOLO para demostracion del dashboard.** Sus filas no
corresponden a ninguna iniciativa real: los codigos son `DEMO-...`, los nombres
son genericos y cada fila es una combinacion aleatoria. Es verosimil en agregado
(proporciones y distribuciones calcadas del real) pero ficticio en el detalle.
**No usarlo para reporteria, informes institucionales ni acreditacion.**

## El real como hoja de ruta de captura

Las columnas vacias del dataset real no son un error: marcan datos que el
instrumento de VcM **no captura hoy** y que deberia empezar a registrar si la
contraparte quiere esas metricas con datos verdaderos (empleadores, desglose por
rol, internacionalizacion, comuna, semestre, ciclo, y actividades ejecutadas,
que existia en 2022-2023 y dejo de capturarse desde 2024).

## Esquema completo

Estado en el real: **Real** = poblado con datos verdaderos (se indica desde que
anio), **Vacia** = presente en el esquema pero sin fuente (NaN en todas las filas).

### Identificacion

| Columna | Tipo | Estado en el real | Descripcion |
|---------|------|-------------------|-------------|
| codigo | str | Real (2022) | Codigo SISAV. Vacio en el instrumento CENTRALIZADAS; usar `nombre_iniciativa` como respaldo. |
| nombre_iniciativa | str | Real (2022) | Nombre de la iniciativa. En el sintetico es un nombre generico de demo. |
| facultad | str | Real (2022) | Facultad (FAE, FCCOT, FCJS, FCNMMA, FCSJ, FHTCS, FING). |
| carrera | str | Real (2022) | Carrera asociada. Coherente con la facultad tambien en el sintetico. |
| instrumento | str | Real (2022) | Instrumento de VcM (EXTENSION, VEDP, VT, FCR, UTG, CENTRALIZADAS). |
| anio | int | Real (2022) | Anio de la convocatoria (2022 a 2025). |
| semestre | str | Vacia | Semestre de ejecucion (1S/2S). No esta en las tablas limpias reales. |
| estado_sisav | str | Real (2022) | Estado en SISAV (vocabulario heterogeneo entre formatos). |

### Participantes desagregados (conteos float, NaN = sin dato, nunca 0 por defecto)

| Columna | Tipo | Estado en el real | Descripcion |
|---------|------|-------------------|-------------|
| n_estudiantes | float | Real (2024) | Estudiantes participantes. NaN en 2022-2023 (la fuente solo traia un total agregado). |
| n_academicos | float | Real (2024) | Academicos/docentes participantes. |
| n_titulados | float | Real (2024) | Titulados participantes. |
| n_empleadores | float | Vacia | Emprendedores/empleadores. **No existe en ninguna fuente real** (confirmado por el diagnostico del notebook 06). |
| n_organizaciones_osc | float | Real (2024) | Organizaciones/instituciones del medio externo. |

### Desglose por rol (charlista / expositor / asistente)

| Columna | Tipo | Estado en el real |
|---------|------|-------------------|
| n_titulados_charlista, n_titulados_expositor, n_titulados_asistente | float | Vacia |
| n_empleadores_charlista, n_empleadores_expositor, n_empleadores_asistente | float | Vacia |
| n_organizaciones_osc_charlista, n_organizaciones_osc_expositor, n_organizaciones_osc_asistente | float | Vacia |

La fuente real no registra roles. En el sintetico el desglose **suma exacto** al
total de su categoria (verificado con assert).

### Competencias

| Columna | Tipo | Estado en el real | Descripcion |
|---------|------|-------------------|-------------|
| competencia_sello | str multivalor (`; `) | Real (2022) | Competencias sello. En 2022-2023 proviene de `Sello Institucional`. |
| sello_tecnologia | bool | Real (2022) | Flag derivado del texto de `competencia_sello` (normaliza variantes TECNOLOGIA/Tecnologia). NA donde no hay sello. |
| sello_responsabilidad_social | bool | Real (2022) | Flag derivado (RESPONSABILIDAD_SOCIAL / Responsabilidad social). |
| sello_sustentabilidad | bool | Real (2022) | Flag derivado (SUSTENTABILIDAD / Sostenibilidad). |
| sello_genero | bool | Real (2022) | Flag derivado (Genero). |
| competencia_generica | str multivalor (`; `) | Real (2024) | Competencias genericas. No existe en el formato 2022-2023. |

### Dominios disciplinares

| Columna | Tipo | Estado en el real | Descripcion |
|---------|------|-------------------|-------------|
| dominios_disciplinares | str multivalor (`; `) | Real (2024, ~88%) | Dominios disciplinares asociados a la iniciativa (base del KPI 1). Existe en la fuente solo desde 2024; NaN en 2022-2023 (concepto distinto del area generica de esos anios). Separadores de origen normalizados (`;`, salto de linea y `., ` del formato 2024); no se divide por coma simple porque las frases tienen comas internas. `No aplica` se trata como sin dato. |

### Otros indicadores

| Columna | Tipo | Estado en el real | Descripcion |
|---------|------|-------------------|-------------|
| ciclo_estudio | int (0/1/2/3) | Vacia | Ciclo del modelo educativo. No esta en las tablas limpias reales. |
| internacionalizacion | bool | Vacia | Si la iniciativa tiene componente internacional. No se captura en la fuente. |
| catedra_asignatura | str | Real (2024, parcial ~57%) | Nombre de la catedra/asignatura asociada. Cobertura parcial por instrumento. |
| comuna_rm | str | Vacia | Comuna de la Region Metropolitana donde se ejecuta. No se captura. En el sintetico son comunas reales de la RM. |
| evidencia | str (SI/NO) | Real (2022, 96-100%) | Si la iniciativa cuenta con evidencia de ejecucion. Normalizada desde la fuente: 2022-2023 se deriva de `Estado de Evidencia` (COMPLETO/INCOMPLETO -> SI, SIN EVIDENCIA -> NO); 2024-2025 traen el campo SI/NO directo. En el sintetico se genera con la proporcion real observada de SI (~85%). |

### KPI I19

| Columna | Tipo | Estado en el real | Descripcion |
|---------|------|-------------------|-------------|
| cantidad_act_planificadas | float | Real (2022, 96-98%) | Actividades planificadas, recuperada de la fuente en todos los anios. Celdas sucias tipo `2; 3` se resuelven tomando el primer numero. |
| cantidad_act_ejecutadas | float | Real (solo 2022-2023, 78-90%) | Actividades ejecutadas. La fuente dejo de capturarla desde 2024: NaN en 2024-2025. El KPI I19 real (ejecutadas/planificadas) es calculable solo para 2022-2023. En el sintetico esta poblada en todos los anios y nunca supera a planificadas (verificado con assert). |

### Linaje

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| _archivo_origen | str | Archivo fuente real, o `generador_sintetico_seed42`. |
| _anio | int | Anio de linaje (igual a `anio`). |
| _origen_dato | str | `"real"` o `"sintetico"`. |

## Como se calco el sintetico del real

- **Vocabularios reales** extraidos del dataset real (facultades, carreras,
  instrumentos, estados, competencias, dominios disciplinares, catedras). No se
  inventaron nombres. Los dominios sinteticos se remuestrean de los valores
  reales 2024-2025 y se pueblan en todos los anios.
- **Proporciones reales**: bootstrap por anio del bloque categorico completo
  `(facultad, carrera, instrumento, estado)`, preservando la distribucion
  conjunta y el patron temporal (mismas filas por anio que el real: 2022=148,
  2023=157, 2024=176, 2025=345; 2025 es el anio con mas iniciativas).
- **Distribuciones numericas reales**: los conteos se remuestrean de la
  distribucion empirica real 2024-2025 (preserva min, max, media, mediana y
  desviacion; la comparacion se imprime en el notebook).
- **Sin analogo real**: `n_empleadores` se remuestrea de la distribucion de
  organizaciones (orden de magnitud analogo, supuesto documentado).
- **Evidencia**: SI/NO con la proporcion real observada de SI (~85%), no 50/50
  arbitrario.
- **Seed fijo 42**: la generacion es reproducible.

## Verificaciones que hace el notebook (fallan si no se cumplen)

1. Columnas identicas en nombre y orden entre real y sintetico.
2. Mismo numero de filas por anio en ambos.
3. Roles suman exacto al total de su categoria; ejecutadas <= planificadas;
   comunas dentro de la lista real de la RM; sintetico 100% poblado.
4. Ningun nombre de iniciativa real aparece en el sintetico.
