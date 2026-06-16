"""Utilidades compartidas: versión del pipeline, paths, logging."""

from pathlib import Path

PIPELINE_VERSION = "0.1.0"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_SAMPLE = PROJECT_ROOT / "data" / "sample"
DATA_STAGING = PROJECT_ROOT / "data" / "staging"
DATA_CLEAN = PROJECT_ROOT / "data" / "clean"
