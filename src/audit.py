"""Módulo central de auditoría: modificación-con-registro.

Centraliza la lógica para que toda transformación que altere un valor
quede registrada en el audit log con trazabilidad completa.
"""

import pandas as pd


def _ambos_nulos(a, b) -> bool:
    """Retorna True si ambos valores son nulos (NaN/None)."""
    return pd.isna(a) and pd.isna(b)


def _valores_iguales(original, nuevo) -> bool:
    """Compara dos valores manejando NaN correctamente."""
    if _ambos_nulos(original, nuevo):
        return True
    if pd.isna(original) or pd.isna(nuevo):
        return False
    return original == nuevo


def aplicar_y_registrar(
    df: pd.DataFrame,
    indice: int,
    columna: str,
    valor_nuevo,
    regla_id: str,
    audit_log: list[dict],
) -> None:
    """Modifica un valor en el DataFrame y registra la operación en el audit log.

    Solo modifica y registra si el valor efectivamente cambia.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame en proceso de transformación (se muta in-place).
    indice : int
        Índice de la fila a modificar.
    columna : str
        Nombre de la columna a modificar.
    valor_nuevo :
        Valor resultante tras la transformación.
    regla_id : str
        ID estable de la regla (e.g. "R-001").
    audit_log : list[dict]
        Lista mutable donde se acumulan los registros de auditoría.
    """
    valor_original = df.at[indice, columna]

    if _valores_iguales(valor_original, valor_nuevo):
        return

    df.at[indice, columna] = valor_nuevo

    audit_log.append({
        "codigo_iniciativa": df.at[indice, "Codigo"],
        "columna": columna,
        "valor_original": valor_original,
        "valor_resultante": valor_nuevo,
        "regla_id": regla_id,
        "archivo_origen": df.at[indice, "_archivo_origen"],
    })
