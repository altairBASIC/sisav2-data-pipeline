"""Ingesta: lectura de archivos Excel y extracción de metadatos del filename.

Responsabilidades:
- Leer cada .xlsx de un directorio de entrada.
- Parsear el nombre del archivo para extraer: instrumento, convocatoria, descripción.
- Añadir columnas de linaje.
- Validar contra el esquema canónico de 36 columnas.
- Concatenar todos los DataFrames conformes en uno solo (staging).

Diseñado para que añadir un origen alternativo (e.g. conexión a BD SISAV2)
sea un cambio aditivo sin refactorizar el pipeline.
"""

import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from src.schema import COLUMNAS_CANONICAS, COLUMNAS_LINAJE
from src.utils import PIPELINE_VERSION


class SchemaError(Exception):
    """Raised when a file does not match the canonical schema."""


# Vocabulario controlado de instrumentos reales, ordenado por especificidad
# (más específico primero para que el match sea unívoco).
# Se usa (?:^|_) y (?:_|$) como boundaries dado que _ es word-char en regex.
INSTRUMENTOS_CONOCIDOS: list[tuple[str, str]] = [
    (r"VEDP|Vinculaci[oó]n_con_el_Entorno_Disciplinar_Profesional", "VEDP"),
    (r"VEPR", "VEPR"),
    (r"(?:^|_)VT(?:_|$)|Vinculaci[oó]n_con_Titulados", "VT"),
    (r"Extensi[oó]n_Acad[eé]mica|(?:^|_)EXTENSION(?:_|$)", "EXTENSION"),
    (r"(?:^|_)UET(?:_|$)", "UET"),
    (r"(?:^|_)A_S(?:_|$)|Aprendizaje.*Servicio", "A+S"),
    (r"CHARLAS", "CHARLAS"),
    (r"SEMINARIO", "SEMINARIO"),
    (r"libros_editorial", "EDITORIAL"),
    (r"INICIATIVAS", "INICIATIVAS"),
    (r"(?:^|_)OTRO(?:_|$)", "OTRO"),
]


def _detectar_instrumento(descripcion: str) -> str:
    """Identifica el instrumento real buscando en la descripción."""
    for pattern, nombre in INSTRUMENTOS_CONOCIDOS:
        if re.search(pattern, descripcion):
            return nombre
    return "DESCONOCIDO"


def parsear_nombre_archivo(filename: str) -> dict:
    """Extrae metadatos codificados en el nombre del archivo.

    Convención observada en los exports reales:
        {NIVEL}__{convNN}__{descripcion}.xlsx

    El nivel (PRE_GRADO, POST_GRADO, EXTENSION) es la clasificación
    administrativa. El instrumento real se detecta dentro de la descripción.

    Returns
    -------
    dict con claves: nivel, instrumento, convocatoria, anio, semestre, descripcion
    """
    stem = Path(filename).stem

    pattern = r"^(?P<nivel>[A-Z_]+)__conv(?P<conv_num>\d+)__(?P<descripcion>.+)$"
    match = re.match(pattern, stem)

    if not match:
        return {
            "nivel": "DESCONOCIDO",
            "instrumento": "DESCONOCIDO",
            "convocatoria": "DESCONOCIDO",
            "anio": None,
            "semestre": None,
            "descripcion": stem,
        }

    nivel = match.group("nivel")
    conv_num = match.group("conv_num")
    descripcion = match.group("descripcion")

    instrumento = _detectar_instrumento(descripcion)

    anio_match = re.search(r"(20\d{2})", descripcion)
    anio = int(anio_match.group(1)) if anio_match else None

    semestre = None
    if re.search(r"1er[_ ]Semestre|1[_ ]Semestre|_1S", descripcion):
        semestre = "1S"
    elif re.search(r"2do[_ ]Semestre|2[_ ]Semestre|_2S|_2d$", descripcion):
        semestre = "2S"

    return {
        "nivel": nivel,
        "instrumento": instrumento,
        "convocatoria": f"conv{conv_num}",
        "anio": anio,
        "semestre": semestre,
        "descripcion": descripcion,
    }


def validar_esquema(df: pd.DataFrame, filename: str) -> None:
    """Valida que el DataFrame tenga exactamente las 36 columnas canónicas.

    Raises
    ------
    SchemaError
        Si las columnas no coinciden, detallando cuáles sobran y cuáles faltan.
    """
    cols_actual = list(df.columns)
    cols_esperadas = set(COLUMNAS_CANONICAS)
    cols_actual_set = set(cols_actual)

    extra = cols_actual_set - cols_esperadas
    faltantes = cols_esperadas - cols_actual_set

    if extra or faltantes:
        msg_parts = [f"Esquema no conforme en '{filename}' ({len(cols_actual)} columnas)."]
        if faltantes:
            msg_parts.append(f"  Faltan ({len(faltantes)}): {sorted(faltantes)}")
        if extra:
            msg_parts.append(f"  Sobran ({len(extra)}): {sorted(extra)}")
        raise SchemaError("\n".join(msg_parts))


def leer_excels(
    directorio: str | Path,
    strict: bool = True,
) -> tuple[pd.DataFrame, list[dict]]:
    """Lee todos los .xlsx del directorio y retorna un DataFrame consolidado.

    Parameters
    ----------
    directorio :
        Ruta al directorio con archivos Excel.
    strict :
        Si True, los archivos que no conforman el esquema se reportan
        y se excluyen (no se rompe la corrida completa).
        Si False, falla al primer archivo no conforme.

    Returns
    -------
    tuple[pd.DataFrame, list[dict]]
        - DataFrame consolidado con columnas de linaje añadidas.
        - Lista de dicts con info de archivos rechazados (filename, motivo).
    """
    directorio = Path(directorio)
    archivos = sorted(directorio.glob("*.xlsx"))

    if not archivos:
        raise FileNotFoundError(f"No se encontraron archivos .xlsx en {directorio}")

    frames: list[pd.DataFrame] = []
    rechazados: list[dict] = []
    fecha_proceso = datetime.now(timezone.utc).isoformat(timespec="seconds")

    for archivo in archivos:
        df = pd.read_excel(archivo, engine="openpyxl")
        meta = parsear_nombre_archivo(archivo.name)

        try:
            validar_esquema(df, archivo.name)
        except SchemaError as e:
            if strict:
                rechazados.append({"archivo": archivo.name, "motivo": str(e)})
                continue
            else:
                raise

        df["_archivo_origen"] = archivo.name
        df["_nivel"] = meta["nivel"]
        df["_instrumento"] = meta["instrumento"]
        df["_convocatoria"] = meta["convocatoria"]
        df["_anio"] = meta["anio"]
        df["_semestre"] = meta["semestre"]
        df["_fecha_proceso"] = fecha_proceso
        df["_version_pipeline"] = PIPELINE_VERSION

        frames.append(df)

    if not frames:
        raise SchemaError(
            f"Ningún archivo de {directorio} conforma el esquema canónico. "
            f"Rechazados: {len(rechazados)}"
        )

    consolidado = pd.concat(frames, ignore_index=True)

    expected_cols = COLUMNAS_CANONICAS + COLUMNAS_LINAJE
    consolidado = consolidado[expected_cols]

    return consolidado, rechazados
