"""Reglas de limpieza y transformación.

Cada función de regla:
- Tiene un ID estable (R-XXX) como constante al inicio.
- Usa audit.aplicar_y_registrar() para toda modificación atómica.
- Está documentada aquí y en docs/reglas_transformacion.md.
"""

import re

import pandas as pd

from src.audit import aplicar_y_registrar
from src.schema import COLUMNAS_CANONICAS

# Columnas de texto sobre las que operan R-001 y R-002
_COLS_TEXTO = [c for c in COLUMNAS_CANONICAS if c not in (
    "N", "Monto", "Fecha Inicio", "Fecha Termino",
)]

# Columnas multivalor para R-003 (separador "; " o " / ")
_COLS_MULTIVALOR = [
    "ODS",
    "Competencia Sello",
    "Área de influencia",
    "Competencia genérica",
    "PDI",
]


def r001_normalizar_espacios(df: pd.DataFrame, audit_log: list[dict]) -> pd.DataFrame:
    """R-001: Strip de espacios iniciales/finales y colapso de múltiples espacios."""
    REGLA_ID = "R-001"

    for col in _COLS_TEXTO:
        if col not in df.columns:
            continue
        for idx in df.index:
            val = df.at[idx, col]
            if pd.isna(val) or not isinstance(val, str):
                continue
            limpio = " ".join(val.split())
            if limpio != val:
                aplicar_y_registrar(df, idx, col, limpio, REGLA_ID, audit_log)

    return df


def r002_reemplazar_control(df: pd.DataFrame, audit_log: list[dict]) -> pd.DataFrame:
    """R-002: Reemplaza tabs y newlines internos por espacio simple."""
    REGLA_ID = "R-002"

    for col in _COLS_TEXTO:
        if col not in df.columns:
            continue
        for idx in df.index:
            val = df.at[idx, col]
            if pd.isna(val) or not isinstance(val, str):
                continue
            if "\t" in val or "\n" in val or "\r" in val:
                limpio = re.sub(r"[\t\n\r]+", " ", val)
                limpio = " ".join(limpio.split())
                if limpio != val:
                    aplicar_y_registrar(df, idx, col, limpio, REGLA_ID, audit_log)

    return df


def r003_puntos_multivalor(df: pd.DataFrame, audit_log: list[dict]) -> pd.DataFrame:
    """R-003: Elimina punto final de cada ítem en campos multivalor."""
    REGLA_ID = "R-003"

    def limpiar_items(valor: str) -> str:
        if "; " in valor:
            sep = "; "
        elif " / " in valor:
            sep = " / "
        else:
            return valor.rstrip(".")

        items = valor.split(sep)
        items_limpios = [item.rstrip(".") for item in items]
        return sep.join(items_limpios)

    for col in _COLS_MULTIVALOR:
        if col not in df.columns:
            continue
        for idx in df.index:
            val = df.at[idx, col]
            if pd.isna(val) or not isinstance(val, str):
                continue
            if "." not in val:
                continue
            limpio = limpiar_items(val)
            if limpio != val:
                aplicar_y_registrar(df, idx, col, limpio, REGLA_ID, audit_log)

    return df


def r004_parsear_fechas(df: pd.DataFrame, audit_log: list[dict]) -> pd.DataFrame:
    """R-004: Convierte Fecha Inicio y Fecha Termino de DD/MM/YYYY a datetime."""
    REGLA_ID = "R-004"

    for col in ("Fecha Inicio", "Fecha Termino"):
        if col not in df.columns:
            continue
        originales = df[col].copy()
        parsed = pd.to_datetime(originales, format="%d/%m/%Y", errors="coerce", dayfirst=True)

        # Registrar en audit log antes de reemplazar la columna
        for idx in df.index:
            val_orig = originales.at[idx]
            val_nuevo = parsed.at[idx]
            if pd.isna(val_orig):
                continue
            # Solo registrar valores no parseables (se convierten a NaT)
            if pd.isna(val_nuevo):
                audit_log.append({
                    "codigo_iniciativa": df.at[idx, "Codigo"],
                    "columna": col,
                    "valor_original": val_orig,
                    "valor_resultante": None,
                    "regla_id": REGLA_ID,
                    "archivo_origen": df.at[idx, "_archivo_origen"],
                })

        # Reemplazar la columna completa (cambia dtype a datetime64)
        df[col] = parsed

    return df


def r005_normalizar_semestre(df: pd.DataFrame, audit_log: list[dict]) -> pd.DataFrame:
    """R-005: Normaliza Semestre Ejecución a vocabulario controlado."""
    REGLA_ID = "R-005"
    COL = "Semestre Ejecución"

    if COL not in df.columns:
        return df

    def clasificar(val: str) -> str:
        v = val.strip().lower()
        if re.search(r"primer|1er|1°|^1\s*sem", v):
            return "1S"
        if re.search(r"segund|2do|2°|^2\s*sem|^2do", v):
            return "2S"
        if re.search(r"anual|1er y 2do|1° y 2°|2 semestre[s]$", v):
            return "Anual"
        return "Otro"

    for idx in df.index:
        val = df.at[idx, COL]
        if pd.isna(val) or not isinstance(val, str):
            continue
        normalizado = clasificar(val)
        if normalizado != val:
            aplicar_y_registrar(df, idx, COL, normalizado, REGLA_ID, audit_log)

    return df


def r009_punto_final_nombre(df: pd.DataFrame, audit_log: list[dict]) -> pd.DataFrame:
    """R-009: Elimina punto final en títulos cortos de Nombre de la iniciativa."""
    REGLA_ID = "R-009"
    COL = "Nombre de la iniciativa"

    if COL not in df.columns:
        return df

    for idx in df.index:
        val = df.at[idx, COL]
        if pd.isna(val) or not isinstance(val, str):
            continue
        if val.endswith(".") and len(val) < 100:
            limpio = val.rstrip(".")
            aplicar_y_registrar(df, idx, COL, limpio, REGLA_ID, audit_log)

    return df


def aplicar_todas(df: pd.DataFrame, audit_log: list[dict]) -> pd.DataFrame:
    """Aplica todas las reglas en orden estable.

    Returns
    -------
    pd.DataFrame
        DataFrame limpio tras aplicar todas las reglas.
    """
    df = r001_normalizar_espacios(df, audit_log)
    df = r002_reemplazar_control(df, audit_log)
    df = r003_puntos_multivalor(df, audit_log)
    df = r004_parsear_fechas(df, audit_log)
    df = r005_normalizar_semestre(df, audit_log)
    df = r009_punto_final_nombre(df, audit_log)
    return df
