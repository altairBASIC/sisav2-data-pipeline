"""Definición del esquema canónico de 36 columnas de SISAV2.

Este módulo es la fuente de verdad para validar que los DataFrames
ingestados tienen la estructura esperada.

Esquema derivado del formato "legacy" compartido por 33 de 43 archivos
(convocatorias 2016–2024 y la de extensión 2027). Los 10 archivos restantes
(convocatorias 2025-2S y 2026-1S) usan formularios expandidos con columnas
diferentes; se reportan como no conformes al esquema canónico.
"""

COLUMNAS_CANONICAS: list[str] = [
    "N",
    "Codigo",
    "PLATAFORMA",
    "Facultad",
    "UA",
    "Carrera",
    "Nombre de la iniciativa",
    "Dominios disciplinares",
    "Área",
    "Dimensión",
    "Actividad",
    "Competencia Sello",
    "Contribución Interna",
    "Contribución Externa",
    "Competencia genérica",
    "Perfil del entorno disciplinar y/o profesional",
    "PDI",
    "ODS",
    "Objetivo específico electivo",
    "Estado SISAV",
    "Modalidad",
    "Semestre Ejecución",
    "Cantidad Act Planificadas",
    "Fecha Inicio",
    "Fecha Termino",
    "N estudiantes",
    "N Docentes",
    "N Titulados",
    "N Instituciones del medio externo participantes",
    "Total",
    "Grupo de interés",
    "Área de influencia",
    "Tipo de requerimientos",
    "Monto",
    "Evidencia",
    "Comentarios",
]

COLUMNAS_LINAJE: list[str] = [
    "_archivo_origen",
    "_nivel",
    "_instrumento",
    "_convocatoria",
    "_anio",
    "_semestre",
    "_fecha_proceso",
    "_version_pipeline",
]

N_COLUMNAS_CANONICAS = 36

assert len(COLUMNAS_CANONICAS) == N_COLUMNAS_CANONICAS, (
    f"Se esperan {N_COLUMNAS_CANONICAS} columnas, se encontraron {len(COLUMNAS_CANONICAS)}"
)
