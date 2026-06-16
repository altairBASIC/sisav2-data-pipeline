"""Orquestador del pipeline: ingest → transform → export.

Uso:
    python -m src.main --input data/sample/ --output data/clean/
"""

import argparse

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

    # TODO: Implementar orquestación — esperando confirmación del usuario.
    # 1. ingest.leer_excels(args.input)
    # 2. transform.aplicar_todas(df, audit_log)
    # 3. Exportar df limpio y audit_log a args.output
    raise NotImplementedError("Pendiente de implementación")


if __name__ == "__main__":
    main()
