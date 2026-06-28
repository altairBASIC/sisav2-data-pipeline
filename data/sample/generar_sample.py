"""Genera archivos Excel sintéticos que replican el esquema canónico SISAV2.

Uso:
    python data/sample/generar_sample.py

Produce dos archivos .xlsx de ejemplo con datos ficticios para
poder ejecutar el pipeline sin datos reales.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from src.schema import COLUMNAS_CANONICAS

OUTPUT_DIR = Path(__file__).parent


def generar_archivo(filename: str, n_rows: int = 10, seed: int = 42) -> None:
    """Genera un Excel sintético con n_rows filas ficticias."""
    rng = np.random.default_rng(seed)

    data = {
        "N": list(range(1, n_rows + 1)),
        "Codigo": [f"INI-{i:04d}" for i in range(1, n_rows + 1)],
        "PLATAFORMA": ["SISAV2"] * n_rows,
        "Facultad": rng.choice(["Facultad de Ingeniería", "Facultad de Administración y Economía", "Facultad de Humanidades"], n_rows).tolist(),
        "UA": [None] * n_rows,
        "Carrera": [f"Carrera Ficticia {i % 5 + 1}" for i in range(n_rows)],
        "Nombre de la iniciativa": [f"  Iniciativa Ficticia {i}. " if i % 3 == 0 else f"Iniciativa {i}" for i in range(1, n_rows + 1)],
        "Dominios disciplinares": rng.choice(["Dominio A.; Dominio B.", "Dominio C", None], n_rows).tolist(),
        "Área": [None] * n_rows,
        "Dimensión": [None] * n_rows,
        "Actividad": rng.choice(["Ciclos de Charlas y/o Talleres.", "Seminarios.", None], n_rows).tolist(),
        "Competencia Sello": rng.choice(["Tecnología.; Sustentabilidad.", "Responsabilidad Social.", None], n_rows).tolist(),
        "Contribución Interna": rng.choice(["Contribuir al logro.", None], n_rows).tolist(),
        "Contribución Externa": rng.choice(["Contribuir a la difusión.", None], n_rows).tolist(),
        "Competencia genérica": rng.choice(["Competencias genéricas para la ciudadanía\t", "Visión analítica", None], n_rows).tolist(),
        "Perfil del entorno disciplinar y/o profesional": rng.choice([" Perfil ejemplo ", None], n_rows).tolist(),
        "PDI": rng.choice(["Fortalecer la Vinculación.", None], n_rows).tolist(),
        "ODS": rng.choice(["Educación de calidad.; Alianzas.", "Salud y bienestar.", None], n_rows).tolist(),
        "Objetivo específico electivo": rng.choice(["Objetivo electivo ejemplo", None], n_rows).tolist(),
        "Estado SISAV": rng.choice(["Finalizado", "Ejecución", "No-Realizada", "Rechazada"], n_rows).tolist(),
        "Modalidad": [None] * n_rows,
        "Semestre Ejecución": rng.choice(["Primer Semestre", "Segundo Semestre", "Anual", "3 meses", " 2do Semestre "], n_rows).tolist(),
        "Cantidad Act Planificadas": rng.choice(["1", "2", "3", None], n_rows).tolist(),
        "Fecha Inicio": rng.choice(["15/03/2024", "01/08/2024", "10/10/2024", None], n_rows).tolist(),
        "Fecha Termino": rng.choice(["30/06/2024", "15/12/2024", "20/11/2024", None], n_rows).tolist(),
        "N estudiantes": [None] * n_rows,
        "N Docentes": [None] * n_rows,
        "N Titulados": [None] * n_rows,
        "N Instituciones del medio externo participantes": [None] * n_rows,
        "Total": [None] * n_rows,
        "Grupo de interés": rng.choice([" Grupo ejemplo  ", "Estudiantes", None], n_rows).tolist(),
        "Área de influencia": rng.choice(["Sociedad Civil.; Empresa.", "Estado y sus Instituciones.", None], n_rows).tolist(),
        "Tipo de requerimientos": rng.choice(["Servicios de Alimentación.", None], n_rows).tolist(),
        "Monto": rng.choice([0, 500000, 150000, 0, 1500000], n_rows).tolist(),
        "Evidencia": rng.choice(["SI", "NO"], n_rows).tolist(),
        "Comentarios": [None] * n_rows,
    }

    df = pd.DataFrame(data)
    assert list(df.columns) == COLUMNAS_CANONICAS, (
        f"Columnas no coinciden con esquema canónico: {set(df.columns) ^ set(COLUMNAS_CANONICAS)}"
    )
    output_path = OUTPUT_DIR / filename
    df.to_excel(output_path, index=False, engine="openpyxl")
    print(f"Generado: {output_path} ({n_rows} filas, {len(df.columns)} columnas)")


if __name__ == "__main__":
    generar_archivo("PRE_GRADO__conv90__Convocatoria_EXTENSION_2024.xlsx", n_rows=10, seed=42)
    generar_archivo("PRE_GRADO__conv91__Convocatoria_Proyecto_VcM_1er_Semestre_2024_VEDP.xlsx", n_rows=8, seed=99)
    print("Datos sintéticos generados exitosamente.")
