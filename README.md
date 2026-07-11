# SISAV2 Data Pipeline

Pipeline de datos para el dashboard de Vinculacion con el Medio (VcM) de la
UTEM. Consolida las planillas fuente exportadas desde SISAV2 en datasets limpios
listos para visualizacion, con esquema unificado y documentacion de que se puede
calcular hoy con datos reales y que no.

## Que resuelve

Las iniciativas de VcM se registran en planillas Excel que cambian de formato
segun el anio y el instrumento: distinto numero de columnas, nombres distintos y
campos que aparecen o desaparecen entre convocatorias. Este repositorio absorbe
esa heterogeneidad y entrega dos datasets intercambiables para el dashboard,
mas el analisis de cobertura de los KPIs oficiales solicitados por VcM.

## Flujo de trabajo (notebooks)

El trabajo reproducible esta en `notebooks/`, en este orden:

| Notebook | Que hace |
|----------|----------|
| `01_perfilado` | Perfilado de calidad del formato base. |
| `02_comparacion_formatos` | Compara formato legacy vs expandido. |
| `03_exploracion_planillas_origen` | Caracteriza las planillas fuente por convocatoria. |
| `04_consolidado_indicadores` | Primer consolidado y limpieza de las familias de formato. |
| `05_validacion_y_resumen` | Validacion del consolidado y resumen ejecutivo. |
| `06_viabilidad_columnas` | Diagnostico de que columnas pedidas por el dashboard existen (o no) en la fuente. |
| `07_extraccion_final` | Extrae dos tablas reales limpias: participantes 2024-2025 e historico 2022-2025. |
| `08_datasets_dashboard` | Arma el esquema unificado y genera `dashboard_real` + `dashboard_sintetico`. |
| `09_comparacion_real_vs_sintetico` | Compara cobertura y similitud estadistica entre ambos datasets. |
| `10_kpis_dashboard` | Visualiza los KPIs oficiales: que alimenta el real hoy y que solo el sintetico puede demostrar. |

Los notebooks se versionan **sin output** para no exponer datos reales en el
historial. Antes de commitear:

```bash
jupyter nbconvert --clear-output --inplace notebooks/*.ipynb
```

Documentacion del esquema: `docs/esquema_dashboard.md`.

## Datasets finales

Ambos salen del notebook 08 con **esquema identico de 39 columnas** (mismo
orden), pensados para ser intercambiables en el dashboard:

| Dataset | Ubicacion | Proposito |
|---------|-----------|-----------|
| **Real** | `data/clean/dashboard_real.{csv,parquet}` | Datos verdaderos de SISAV2 (2022-2025). Las columnas que la fuente no captura estan presentes pero vacias (NaN). |
| **Sintetico** | `data/synthetic/dashboard_sintetico.{csv,parquet}` | Demostrativo: todas las columnas pobladas, estadisticamente calcado del real (proporciones y distribuciones). Ficticio en el detalle. |

La columna `_origen_dato` (`real` / `sintetico`) identifica cada archivo. El
sintetico es solo para demostrar el dashboard completo; **no** debe usarse para
reporteria, informes institucionales ni acreditacion.

## Manejo de datos confidenciales

Los datos reales de VcM (`data/raw/`, `data/staging/`, `data/clean/`) quedan
**fuera del control de versiones** via `.gitignore`.

El dataset sintetico en `data/synthetic/` **si se versiona**: es inventado, no
confidencial, y permite clonar el repositorio y correr los notebooks 09-10 (y
probar el dashboard) sin tener acceso a las planillas reales.

## Estado de los KPIs

El repositorio incluye el analisis de que indicadores oficiales de VcM son
calculables con datos reales hoy y cuales requieren datos que VcM aun no
captura. La foto completa, grafico por grafico, esta en el notebook
`10_kpis_dashboard`.

En resumen:

- Varios KPIs de iniciativas, facultades, instrumentos, participantes
  desagregados (desde 2024) y competencias sello si se pueden armar con el
  dataset real.
- Otros (empleadores, desglose por rol, territorio RM, ciclo,
  internacionalizacion, etc.) solo se demuestran con el sintetico, porque la
  fuente real no los registra.

## Limitaciones documentadas

- **Sin fuente real**: empleadores, roles (charlista / expositor / asistente) y
  territorio RM (comuna), entre otras columnas pedidas al dashboard.
- **Participantes desagregados** (estudiantes, academicos, titulados,
  organizaciones): solo desde 2024; en 2022-2023 esas celdas quedan vacias por
  diseno.
- **KPI I19** (actividades ejecutadas / planificadas): calculable con datos
  reales solo en 2022-2023; desde 2024 la fuente dejo de capturar ejecutadas.

Detalle del esquema y de la cobertura por columna: `docs/esquema_dashboard.md`.

## Estructura del repositorio

```
sisav2-data-pipeline/
├── data/
│   ├── raw/         # Planillas reales (gitignoreado)
│   ├── staging/     # Capa intermedia (gitignoreado)
│   ├── clean/       # Datasets reales limpios (gitignoreado)
│   └── synthetic/   # Dataset sintetico de demostracion (versionado)
├── notebooks/       # Flujo 01-10
├── docs/            # Esquema, diccionarios, reglas, alcance
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Inicio rapido

Requisito: Python 3.10 o superior.

```bash
git clone https://github.com/altairBASIC/sisav2-data-pipeline.git
cd sisav2-data-pipeline

python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux / macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

Para explorar sin datos reales, abrir los notebooks 09 y 10: leen
`data/synthetic/dashboard_sintetico`, que si esta versionado.

Para regenerar los datasets con datos reales, colocar las planillas en
`data/raw/` y ejecutar el flujo desde el notebook 07 (extraccion) y el 08
(esquema unificado). Los artefactos reales se escriben en `data/clean/` y no se
suben al repositorio.

## Autores

Ignacio Ramirez y Claudia Cancino.  
Institucion: Universidad Tecnologica Metropolitana (UTEM).

## Licencia

MIT - ver [LICENSE](LICENSE).
