"""Reglas de limpieza y transformación.

Cada función de regla:
- Tiene un ID estable (R-XXX) como constante al inicio.
- Usa audit.aplicar_y_registrar() para toda modificación atómica.
- Está documentada aquí y en docs/reglas_transformacion.md.
"""

import pandas as pd


def r001_normalizar_espacios(df: pd.DataFrame, audit_log: list[dict]) -> pd.DataFrame:
    """R-001: Normaliza espacios en columnas de texto.

    Elimina espacios iniciales/finales y colapsa múltiples espacios internos.
    """
    REGLA_ID = "R-001"
    # TODO: Implementar lógica — esperando confirmación del usuario.
    raise NotImplementedError("Pendiente de implementación")


def aplicar_todas(df: pd.DataFrame, audit_log: list[dict]) -> pd.DataFrame:
    """Aplica todas las reglas en orden definido.

    Returns
    -------
    pd.DataFrame
        DataFrame limpio tras aplicar todas las reglas.
    """
    # TODO: Encadenar reglas en orden — esperando confirmación del usuario.
    raise NotImplementedError("Pendiente de implementación")
