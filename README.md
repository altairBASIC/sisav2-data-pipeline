# SISAV2 Data Pipeline

Pipeline de consolidación y limpieza de exports Excel del sistema SISAV2 (iniciativas de Vinculación con el Medio) hacia tablas analíticas que alimentan un dashboard institucional.

## Problema que resuelve

Cada convocatoria de SISAV2 se exporta como un archivo Excel independiente. Comparten un esquema de 36 columnas pero difieren en qué campos vienen poblados según año e instrumento. Los metadatos clave (instrumento, año, n° de convocatoria, semestre) están codificados en el nombre del archivo, no como columnas. Este pipeline:

1. Extrae metadatos del nombre de archivo y los incorpora como columnas.
2. Aplica reglas de limpieza documentadas y trazables.
3. Genera un audit log que registra cada modificación atómica.
4. Produce tablas limpias consolidadas listas para análisis.

## Estructura del repositorio

```
sisav2-data-pipeline/
├── data/
│   ├── raw/            # Exports Excel reales (IGNORADOS por .gitignore)
│   ├── sample/         # Datos sintéticos para desarrollo y CI
│   ├── staging/        # Capa intermedia post-ingesta (ignorada)
│   └── clean/          # Tablas finales + audit log (ignoradas)
├── src/
│   ├── __init__.py
│   ├── ingest.py       # Lectura de Excel y extracción de metadatos del filename
│   ├── transform.py    # Reglas de limpieza (cada una con ID estable R-XXX)
│   ├── audit.py        # Función central de modificación-con-registro
│   ├── schema.py       # Definición del esquema esperado (36 columnas)
│   ├── utils.py        # Helpers: paths, logging, versión del pipeline
│   └── main.py         # Orquestador: ingest → transform → export
├── notebooks/          # Exploración y validación ad-hoc
├── docs/
│   ├── diccionario_datos.md       # Esquema de 36 columnas documentado
│   └── reglas_transformacion.md   # Catálogo de reglas R-XXX
├── .gitignore
├── .python-version    # Versión de Python del proyecto (>= 3.11)
├── LICENSE
├── README.md
└── requirements.txt
```

## Inicio rápido

**Requisito**: Python >= 3.11 (ver `.python-version`).

```bash
# 1. Clonar
git clone https://github.com/altairBASIC/sisav2-data-pipeline.git
cd sisav2-data-pipeline

# 2. Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar con datos de ejemplo
python -m src.main --input data/sample/ --output data/clean/
```

Para usar datos reales, colocar los exports `.xlsx` en `data/raw/` y cambiar `--input data/raw/`.

## Trazabilidad y linaje

Cada fila en las tablas limpias incluye:

| Columna | Descripción |
|---------|-------------|
| `_archivo_origen` | Nombre del archivo Excel fuente |
| `_convocatoria` | Identificador de convocatoria (extraído del filename) |
| `_fecha_proceso` | Timestamp ISO 8601 de la corrida |
| `_version_pipeline` | Tag semántico del pipeline (e.g. `0.1.0`) |

El **audit log** (`data/clean/audit_log.csv`) registra cada modificación atómica:

| Columna | Descripción |
|---------|-------------|
| `codigo_iniciativa` | Identificador de la iniciativa modificada |
| `columna` | Columna afectada |
| `valor_original` | Valor antes de la transformación |
| `valor_resultante` | Valor después de la transformación |
| `regla_id` | ID estable de la regla (e.g. `R-001`) |
| `archivo_origen` | Archivo del que proviene el registro |

El audit log se regenera completo en cada corrida; el historial lo provee Git sobre el código fuente.

## Convenciones

- **Reglas de limpieza**: cada regla tiene un ID estable `R-XXX` presente en `src/transform.py`, en el audit log y en `docs/reglas_transformacion.md`.
- **Commits**: Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`).
- **Versionado**: SemVer en `src/utils.py`.

## Roadmap

Los siguientes ítems están planificados pero **no implementados**:

1. **Containerización OCI** — Containerfile compatible con Podman y Docker. Los datos se montarán como volumen (`-v ./data/raw:/data/raw:ro`); nunca dentro de la imagen. La estructura de carpetas ya soporta esta separación.

2. **Conector de base de datos SISAV2** — Adaptación de `src/ingest.py` para leer directamente desde una instancia local de SISAV2 (PostgreSQL/SQL Server) cuando esté disponible, además de los Excel. La interfaz de ingesta está diseñada para que añadir un nuevo origen sea un cambio aditivo, sin refactorizar el pipeline.

## Licencia

MIT — ver [LICENSE](LICENSE).
