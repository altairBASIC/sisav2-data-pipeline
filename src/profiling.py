"""Perfilado de datos SISAV2: genera reporte de calidad sobre el DataFrame consolidado.

Uso:
    python -m src.profiling --input <directorio_con_xlsx>

Produce por stdout un reporte con:
- Resumen de ingesta (archivos conformes/rechazados)
- Matriz de cobertura: % de poblado por columna y convocatoria
- Cardinalidad y valores únicos de campos categóricos
- Detección de problemas de suciedad reales
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

from src.ingest import leer_excels
from src.schema import COLUMNAS_CANONICAS


def matriz_cobertura(df: pd.DataFrame) -> pd.DataFrame:
    """Porcentaje de valores no-nulos por columna y convocatoria."""
    cols_datos = COLUMNAS_CANONICAS
    cobertura = (
        df.groupby("_convocatoria")[cols_datos]
        .apply(lambda g: g.notna().mean() * 100)
    )
    return cobertura.round(1)


def resumen_categoricos(df: pd.DataFrame, max_unicos: int = 30) -> dict:
    """Cardinalidad y valores únicos para columnas con <= max_unicos valores distintos."""
    resultado = {}
    for col in COLUMNAS_CANONICAS:
        if col not in df.columns:
            continue
        serie = df[col].dropna()
        if serie.empty:
            resultado[col] = {"cardinalidad": 0, "valores": []}
            continue
        # Solo analizar como categórico si tiene pocos valores únicos
        n_unicos = serie.nunique()
        if n_unicos <= max_unicos:
            valores = serie.value_counts().head(20)
            resultado[col] = {
                "cardinalidad": n_unicos,
                "valores": {str(k): int(v) for k, v in valores.items()},
            }
    return resultado


def detectar_problemas(df: pd.DataFrame) -> dict:
    """Detecta problemas de suciedad comunes en los datos."""
    problemas = {}

    for col in COLUMNAS_CANONICAS:
        if col not in df.columns:
            continue
        serie = df[col]
        col_problemas = []

        # Columnas 100% vacías
        if serie.isna().all():
            col_problemas.append("COLUMNA 100% VACÍA")
            problemas[col] = col_problemas
            continue

        # Solo analizar strings
        str_vals = serie.dropna().astype(str)
        if str_vals.empty:
            continue

        # Espacios/tabs iniciales o finales
        con_padding = str_vals[str_vals != str_vals.str.strip()]
        if len(con_padding) > 0:
            ejemplos = con_padding.head(3).tolist()
            col_problemas.append(
                f"Espacios/tabs: {len(con_padding)} valores con padding "
                f"(ej: {[repr(e) for e in ejemplos]})"
            )

        # Puntos finales en categorías
        con_punto = str_vals[str_vals.str.endswith(".") & (str_vals.str.len() < 100)]
        if len(con_punto) > 0:
            ejemplos = con_punto.value_counts().head(3).index.tolist()
            col_problemas.append(
                f"Puntos finales: {len(con_punto)} valores terminan en '.' "
                f"(ej: {ejemplos})"
            )

        # Mayúsculas inconsistentes (misma categoría con distinto case)
        if serie.nunique() <= 50:
            lower_map = {}
            for val in str_vals.unique():
                key = val.strip().lower()
                lower_map.setdefault(key, []).append(val)
            inconsistentes = {k: v for k, v in lower_map.items() if len(v) > 1}
            if inconsistentes:
                ejemplos = list(inconsistentes.values())[:3]
                col_problemas.append(
                    f"Case inconsistente: {len(inconsistentes)} grupos "
                    f"(ej: {ejemplos})"
                )

        # Campos multivalor con separador
        con_separador = str_vals[
            str_vals.str.contains(r"[;|/,]", regex=True, na=False)
            & (str_vals.str.len() < 200)
        ]
        if len(con_separador) > 5:
            ejemplos = con_separador.head(3).tolist()
            col_problemas.append(
                f"Posible multivalor: {len(con_separador)} valores con separadores "
                f"(ej: {[e[:60] for e in ejemplos]})"
            )

        # Tildes inconsistentes (variantes con/sin tilde del mismo token)
        if serie.nunique() <= 50:
            import unicodedata
            def sin_tildes(s):
                return "".join(
                    c for c in unicodedata.normalize("NFD", s)
                    if unicodedata.category(c) != "Mn"
                )
            norm_map = {}
            for val in str_vals.unique():
                key = sin_tildes(val.strip().lower())
                norm_map.setdefault(key, []).append(val)
            tilde_incon = {
                k: v for k, v in norm_map.items()
                if len(v) > 1 and any(sin_tildes(x) != x for x in v)
            }
            if tilde_incon:
                ejemplos = list(tilde_incon.values())[:3]
                col_problemas.append(
                    f"Tildes inconsistentes: {len(tilde_incon)} grupos "
                    f"(ej: {ejemplos})"
                )

        # Montos en 0
        if col == "Monto":
            try:
                montos = pd.to_numeric(serie, errors="coerce")
                ceros = (montos == 0).sum()
                if ceros > 0:
                    col_problemas.append(f"Montos en 0: {ceros} registros")
            except Exception:
                pass

        if col_problemas:
            problemas[col] = col_problemas

    return problemas


def generar_reporte(directorio: str | Path) -> str:
    """Genera el reporte completo de perfilado como texto."""
    lines: list[str] = []
    sep = "=" * 80

    lines.append(sep)
    lines.append("  REPORTE DE PERFILADO — SISAV2 DATA PIPELINE")
    lines.append(sep)
    lines.append("")

    # --- Ingesta ---
    df, rechazados = leer_excels(directorio, strict=True)
    lines.append(f"■ INGESTA")
    lines.append(f"  Directorio: {directorio}")
    lines.append(f"  Archivos conformes (36 cols): {df['_archivo_origen'].nunique()}")
    lines.append(f"  Filas consolidadas: {df.shape[0]}")
    lines.append(f"  Archivos rechazados (esquema diferente): {len(rechazados)}")
    for r in rechazados:
        lines.append(f"    ✗ {r['archivo'][:80]}")
    lines.append("")

    # --- Distribución por convocatoria ---
    lines.append(f"■ FILAS POR CONVOCATORIA")
    dist = df.groupby(["_convocatoria", "_instrumento", "_anio"]).size().reset_index(name="filas")
    dist = dist.sort_values("_convocatoria")
    for _, row in dist.iterrows():
        lines.append(f"  {row['_convocatoria']:8s}  {row['_instrumento']:12s}  año={row['_anio']}  filas={row['filas']}")
    lines.append(f"  {'TOTAL':8s}  {' ':12s}  {' ':8s}  filas={df.shape[0]}")
    lines.append("")

    # --- Matriz de cobertura ---
    lines.append(f"■ MATRIZ DE COBERTURA (% no-nulo por columna × convocatoria)")
    cob = matriz_cobertura(df)
    lines.append("")

    # Columnas 100% vacías globalmente
    global_pct = df[COLUMNAS_CANONICAS].notna().mean() * 100
    vacias = global_pct[global_pct == 0].index.tolist()
    parciales = global_pct[(global_pct > 0) & (global_pct < 100)].sort_values()

    lines.append(f"  Columnas 100% vacías globalmente ({len(vacias)}):")
    for c in vacias:
        lines.append(f"    • {c}")
    lines.append("")

    lines.append(f"  Columnas parcialmente pobladas ({len(parciales)}):")
    for c, pct in parciales.items():
        lines.append(f"    • {c}: {pct:.1f}% global")
    lines.append("")

    lines.append(f"  Columnas 100% pobladas ({(global_pct == 100).sum()}):")
    for c in global_pct[global_pct == 100].index:
        lines.append(f"    • {c}")
    lines.append("")

    # Detalle por convocatoria para columnas parciales
    if len(parciales) > 0:
        lines.append("  Detalle cobertura de columnas parciales por convocatoria:")
        for col in parciales.index:
            col_cob = cob[col] if col in cob.columns else pd.Series(dtype=float)
            nonzero = col_cob[col_cob > 0]
            if not nonzero.empty:
                detalle = ", ".join(f"{idx}={v:.0f}%" for idx, v in nonzero.items())
                lines.append(f"    {col}: {detalle}")
        lines.append("")

    # --- Categóricos ---
    lines.append(f"■ CAMPOS CATEGÓRICOS (≤30 valores únicos)")
    cats = resumen_categoricos(df)
    for col, info in sorted(cats.items(), key=lambda x: x[1]["cardinalidad"]):
        lines.append(f"  {col} (cardinalidad={info['cardinalidad']}):")
        if info["valores"]:
            for val, count in list(info["valores"].items())[:10]:
                lines.append(f"    {val!r:50s} → {count}")
            if len(info["valores"]) > 10:
                lines.append(f"    ... y {len(info['valores']) - 10} más")
        lines.append("")

    # --- Problemas de suciedad ---
    lines.append(f"■ PROBLEMAS DE SUCIEDAD DETECTADOS")
    probs = detectar_problemas(df)
    if not probs:
        lines.append("  (ninguno detectado)")
    else:
        for col, issues in sorted(probs.items()):
            lines.append(f"  [{col}]")
            for issue in issues:
                lines.append(f"    → {issue}")
            lines.append("")

    lines.append(sep)
    lines.append("  FIN DEL REPORTE")
    lines.append(sep)

    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perfilado de datos SISAV2")
    parser.add_argument("--input", required=True, help="Directorio con .xlsx")
    args = parser.parse_args()

    reporte = generar_reporte(args.input)
    print(reporte)
