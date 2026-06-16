"""Genera archivos Excel sintéticos que replican el esquema SISAV2.

Uso:
    python data/sample/generar_sample.py

Produce dos archivos .xlsx de ejemplo con datos ficticios para
poder ejecutar el pipeline sin datos reales.
"""

import pandas as pd
import numpy as np
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent

COLUMNAS = [
    "codigo_iniciativa",
    "nombre_iniciativa",
    "estado",
    "facultad",
    "carrera",
    "docente_responsable",
    "rut_docente",
    "email_docente",
    "socio_comunitario",
    "rut_socio",
    "tipo_socio",
    "region",
    "comuna",
    "direccion_socio",
    "telefono_socio",
    "email_socio",
    "fecha_inicio",
    "fecha_termino",
    "n_estudiantes",
    "horas_totales",
    "asignatura",
    "codigo_asignatura",
    "objetivos",
    "descripcion_actividad",
    "resultados_esperados",
    "indicador_logro",
    "ods_asociado",
    "area_vinculacion",
    "linea_accion",
    "territorio",
    "presupuesto",
    "fuente_financiamiento",
    "productos_entregables",
    "evaluacion_socio",
    "evaluacion_estudiantes",
    "observaciones",
]


def generar_archivo(filename: str, n_rows: int = 10, seed: int = 42) -> None:
    """Genera un Excel sintético con n_rows filas ficticias."""
    rng = np.random.default_rng(seed)

    data = {
        "codigo_iniciativa": [f"INI-{i:04d}" for i in range(1, n_rows + 1)],
        "nombre_iniciativa": [f"Iniciativa Ficticia {i}" for i in range(1, n_rows + 1)],
        "estado": rng.choice(["En ejecución", "Finalizada", "Suspendida"], n_rows).tolist(),
        "facultad": rng.choice(["Ingeniería", "Educación", "Salud", "Ciencias Sociales"], n_rows).tolist(),
        "carrera": [f"Carrera {i % 5 + 1}" for i in range(n_rows)],
        "docente_responsable": [f"Docente Ficticio {i}" for i in range(1, n_rows + 1)],
        "rut_docente": [f"{rng.integers(10000000, 25000000)}-{rng.integers(0,9)}" for _ in range(n_rows)],
        "email_docente": [f"docente{i}@universidad.cl" for i in range(1, n_rows + 1)],
        "socio_comunitario": [f"Organización Ficticia {i}" for i in range(1, n_rows + 1)],
        "rut_socio": [f"{rng.integers(60000000, 80000000)}-{rng.integers(0,9)}" for _ in range(n_rows)],
        "tipo_socio": rng.choice(["ONG", "Municipalidad", "Fundación", "Junta de Vecinos"], n_rows).tolist(),
        "region": rng.choice(["Metropolitana", "Valparaíso", "Biobío"], n_rows).tolist(),
        "comuna": rng.choice(["Santiago", "Viña del Mar", "Concepción", "Rancagua"], n_rows).tolist(),
        "direccion_socio": [f"Calle Ficticia {i * 100}" for i in range(1, n_rows + 1)],
        "telefono_socio": [f"+569{rng.integers(10000000, 99999999)}" for _ in range(n_rows)],
        "email_socio": [f"socio{i}@org.cl" for i in range(1, n_rows + 1)],
        "fecha_inicio": pd.date_range("2024-03-01", periods=n_rows, freq="7D").strftime("%Y-%m-%d").tolist(),
        "fecha_termino": pd.date_range("2024-07-01", periods=n_rows, freq="7D").strftime("%Y-%m-%d").tolist(),
        "n_estudiantes": rng.integers(5, 40, n_rows).tolist(),
        "horas_totales": rng.integers(20, 200, n_rows).tolist(),
        "asignatura": [f"Asignatura {i % 3 + 1}" for i in range(n_rows)],
        "codigo_asignatura": [f"ASG-{rng.integers(100, 999)}" for _ in range(n_rows)],
        "objetivos": ["Objetivo de ejemplo para datos sintéticos"] * n_rows,
        "descripcion_actividad": ["Descripción ficticia de la actividad"] * n_rows,
        "resultados_esperados": ["Resultado esperado de ejemplo"] * n_rows,
        "indicador_logro": rng.choice(["Alto", "Medio", "Bajo"], n_rows).tolist(),
        "ods_asociado": rng.choice(["ODS 4", "ODS 10", "ODS 11", "ODS 17"], n_rows).tolist(),
        "area_vinculacion": rng.choice(["Educación", "Salud", "Desarrollo local"], n_rows).tolist(),
        "linea_accion": rng.choice(["Aprendizaje Servicio", "Extensión", "Voluntariado"], n_rows).tolist(),
        "territorio": rng.choice(["Urbano", "Rural", "Periurbano"], n_rows).tolist(),
        "presupuesto": rng.integers(100000, 5000000, n_rows).tolist(),
        "fuente_financiamiento": rng.choice(["Institucional", "Externo", "Mixto"], n_rows).tolist(),
        "productos_entregables": ["Informe final, material didáctico"] * n_rows,
        "evaluacion_socio": rng.choice([None, "Satisfactoria", "Regular"], n_rows).tolist(),
        "evaluacion_estudiantes": rng.choice([None, "4.5", "5.0", "6.2"], n_rows).tolist(),
        "observaciones": rng.choice([None, "  Espacios extra  ", "", "Sin observaciones"], n_rows).tolist(),
    }

    df = pd.DataFrame(data)
    output_path = OUTPUT_DIR / filename
    df.to_excel(output_path, index=False, engine="openpyxl")
    print(f"Generado: {output_path} ({n_rows} filas, {len(df.columns)} columnas)")


if __name__ == "__main__":
    generar_archivo("ApS_2024_001_1S.xlsx", n_rows=10, seed=42)
    generar_archivo("ApS_2024_002_2S.xlsx", n_rows=8, seed=99)
    print("Datos sintéticos generados exitosamente.")
