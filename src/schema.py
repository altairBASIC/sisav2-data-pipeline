"""Definición del esquema canónico de 36 columnas de SISAV2.

Este módulo es la fuente de verdad para validar que los DataFrames
ingestados tienen la estructura esperada.
"""

# TODO: Completar con las 36 columnas reales del export SISAV2.
# El orden refleja el orden original del Excel.
COLUMNAS_SISAV2: list[str] = [
    "codigo_iniciativa",
    "nombre_iniciativa",
    # ... 34 columnas restantes por documentar
]

COLUMNAS_LINAJE: list[str] = [
    "_archivo_origen",
    "_convocatoria",
    "_fecha_proceso",
    "_version_pipeline",
]
