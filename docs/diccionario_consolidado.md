# Diccionario del Consolidado de Indicadores

Referencia para el equipo de visualizacion que consume
`data/clean/consolidado_indicadores.csv` o `.parquet`.

## Columnas

| Columna | Tipo | Multivalor | Separador | Desde | Descripcion |
|---------|------|-----------|-----------|-------|-------------|
| codigo | str | No | - | 2022 | Codigo unico de la iniciativa en SISAV2 |
| facultad | str | No | - | 2022 | Facultad responsable |
| carrera | str | No | - | 2022 | Carrera asociada a la iniciativa |
| nombre_iniciativa | str | No | - | 2022 | Nombre o titulo de la iniciativa |
| estado_sisav | str | No | - | 2022 | Estado en SISAV (Finalizado, Ejecucion, Rechazada, etc.) |
| semestre_ejecucion | str | No | - | 2022 | Semestre de ejecucion (Primer Semestre, Segundo Semestre, Anual, etc.) |
| dominios_disciplinares | str | Si | `; ` | 2024 | Dominios disciplinares especificos de la iniciativa. Solo disponible desde 2024. |
| area_generica | str | Si | `; ` | 2022 | Categoria generica de VcM (Relacion con el Entorno, Extension, Titulados, etc.). Solo 2022-2023. |
| competencia_sello | str | Si | `; ` | 2022 | Competencias sello institucionales asociadas |
| actividad | str | No | - | 2022 | Tipo de actividad de la iniciativa |
| ciclo_modelo_educativo | str | No | - | 2022 | Ciclo del modelo educativo (Cientifico Tecnologico, Especializacion, Titulacion). Cobertura parcial. |
| cantidad_act_planificadas | float | No | - | 2022 | Numero de actividades planificadas |
| cantidad_act_ejecutadas | float | No | - | 2022 | Numero de actividades ejecutadas. Solo disponible 2022-2023. |
| n_participantes | float | No | - | 2022 | Total de participantes (sin desglose por genero). |
| ods | str | Si | `; ` | 2022 | Objetivos de Desarrollo Sostenible asociados |
| _archivo_origen | str | No | - | 2022 | Nombre del archivo fuente (trazabilidad) |
| _instrumento | str | No | - | 2022 | Instrumento de VcM derivado del nombre del archivo (EXTENSION, VEDP, VT, FCR, UTG) |
| _anio | int | No | - | 2022 | Año de la convocatoria derivado del nombre del archivo |

## Notas para consumo

- **Separador multivalor**: los campos marcados como multivalor usan `; ` (punto y coma + espacio) como separador. Para obtener una lista, hacer `valor.split("; ")`.
- **NaN**: indica que el dato no existe en la fuente para ese periodo. No es un error; refleja la evolucion del formulario de VcM.
- **cantidad_act_ejecutadas**: solo tiene datos para 2022-2023. Para calcular el KPI I19 (cumplimiento = ejecutadas/planificadas * 100), filtrar por `_anio.isin([2022, 2023])`.
- **dominios_disciplinares vs area_generica**: son conceptos distintos. `dominios_disciplinares` contiene dominios especificos (desde 2024). `area_generica` contiene categorias macro de VcM (solo 2022-2023). No mezclar.
- **Tipos numericos**: las columnas float pueden tener NaN donde no hay dato. Usar `dropna()` antes de operar.

## Archivos de salida

- `data/clean/consolidado_indicadores.csv` - consumo universal
- `data/clean/consolidado_indicadores.parquet` - preserva tipos (recomendado para pandas/polars)
