"""Orquestador del pipeline: ingest → transform → export.

Uso:
    python -m src.main --input data/sample/ --output data/clean/
"""

import argparse
from pathlib import Path

import pandas as pd

from src.ingest import leer_excels
from src.transform import aplicar_todas
from src.utils import PIPELINE_VERSION


def main() -> None:
    """Punto de entrada del pipeline."""
    parser = argparse.ArgumentParser(
        description="Pipeline de consolidación y limpieza SISAV2"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Directorio con archivos .xlsx de entrada",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Directorio de salida para tablas limpias y audit log",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"sisav2-pipeline {PIPELINE_VERSION}",
    )
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # --- Ingesta ---
    print(f"=== SISAV2 Data Pipeline v{PIPELINE_VERSION} ===")
    print(f"Input:  {args.input}")
    print(f"Output: {args.output}")
    print()

    df, rechazados = leer_excels(args.input, strict=True)
    n_conformes = df["_archivo_origen"].nunique()

    print(f"Ingesta: {n_conformes} archivos conformes, {len(rechazados)} rechazados, {len(df)} filas")

    # --- Transformación ---
    audit_log: list[dict] = []
    df = aplicar_todas(df, audit_log)

    # --- Resumen de modificaciones por regla ---
    audit_df = pd.DataFrame(audit_log)
    if not audit_df.empty:
        resumen = audit_df["regla_id"].value_counts().sort_index()
        print(f"\nTransformación: {len(audit_log)} modificaciones registradas")
        for regla, n in resumen.items():
            print(f"  {regla}: {n} modificaciones")
    else:
        print("\nTransformación: 0 modificaciones registradas")

    # --- Export ---
    # Tabla limpia como Parquet y CSV
    out_parquet = output_dir / "sisav2_clean.parquet"
    out_csv = output_dir / "sisav2_clean.csv"
    out_audit = output_dir / "audit_log.csv"
    out_rechazados = output_dir / "archivos_rechazados.csv"

    df.to_parquet(out_parquet, index=False, engine="pyarrow")
    df.to_csv(out_csv, index=False)

    # Audit log
    if audit_log:
        audit_df.to_csv(out_audit, index=False)
    else:
        pd.DataFrame(columns=[
            "codigo_iniciativa", "columna", "valor_original",
            "valor_resultante", "regla_id", "archivo_origen"
        ]).to_csv(out_audit, index=False)

    # Reporte de rechazados
    if rechazados:
        pd.DataFrame(rechazados).to_csv(out_rechazados, index=False)

    print(f"\nExport:")
    print(f"  Tabla limpia: {out_parquet} ({len(df)} filas)")
    print(f"  Tabla limpia: {out_csv}")
    print(f"  Audit log:    {out_audit} ({len(audit_log)} registros)")
    if rechazados:
        print(f"  Rechazados:   {out_rechazados} ({len(rechazados)} archivos)")

    print("\n✓ Pipeline completado exitosamente.")


if __name__ == "__main__":
    main()
