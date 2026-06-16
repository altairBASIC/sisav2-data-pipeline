"""Ingesta: lectura de archivos Excel y extracción de metadatos del filename.

Responsabilidades:
- Leer cada .xlsx de un directorio de entrada.
- Parsear el nombre del archivo para extraer: instrumento, año, n° convocatoria, semestre.
- Añadir columnas de linaje (_archivo_origen, _convocatoria, _fecha_proceso, _version_pipeline).
- Concatenar todos los DataFrames en uno solo (staging).

Diseñado para que añadir un origen alternativo (e.g. conexión a BD SISAV2)
sea un cambio aditivo sin refactorizar el pipeline.
"""

import pandas as pd


def leer_excels(directorio: str) -> pd.DataFrame:
    """Lee todos los .xlsx del directorio y retorna un DataFrame consolidado.

    Parameters
    ----------
    directorio : str
        Ruta al directorio con archivos Excel (data/raw/ o data/sample/).

    Returns
    -------
    pd.DataFrame
        DataFrame consolidado con columnas de linaje añadidas.
    """
    # TODO: Implementar lógica — esperando confirmación del usuario.
    raise NotImplementedError("Pendiente de implementación")


def parsear_nombre_archivo(filename: str) -> dict:
    """Extrae metadatos codificados en el nombre del archivo.

    Convención esperada del filename (a confirmar con datos reales):
        {instrumento}_{año}_{convocatoria}_{semestre}.xlsx

    Parameters
    ----------
    filename : str
        Nombre del archivo (sin ruta).

    Returns
    -------
    dict
        Diccionario con claves: instrumento, anio, convocatoria, semestre.
    """
    # TODO: Implementar lógica — esperando confirmación del usuario.
    raise NotImplementedError("Pendiente de implementación")
