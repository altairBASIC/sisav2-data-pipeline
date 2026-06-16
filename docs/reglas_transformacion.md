# Reglas de Transformación — SISAV2 Data Pipeline

Catálogo de todas las reglas de limpieza aplicadas por el pipeline.
Cada regla tiene un ID estable que aparece en tres lugares:
1. Este documento (explicación y justificación).
2. `src/transform.py` (implementación).
3. Audit log de salida (trazabilidad por registro).

## Estructura de cada regla

| Campo | Descripción |
|-------|-------------|
| **ID** | Identificador estable `R-XXX` |
| **Nombre** | Nombre corto descriptivo |
| **Columnas afectadas** | Lista de columnas sobre las que opera |
| **Descripción** | Qué hace la regla |
| **Justificación** | Por qué se aplica |
| **Tipo** | `normalización`, `imputación`, `descarte`, `corrección` |

---

## R-001 — (Ejemplo) Normalización de espacios en blanco

| Campo | Valor |
|-------|-------|
| **ID** | R-001 |
| **Nombre** | Normalización de espacios |
| **Columnas afectadas** | Todas las columnas de tipo `str` |
| **Descripción** | Elimina espacios iniciales/finales y colapsa espacios múltiples internos a uno solo |
| **Justificación** | Los exports de SISAV2 contienen padding inconsistente que rompe joins y agrupaciones |
| **Tipo** | normalización |

---

> **TODO**: Agregar reglas reales conforme se definan durante el análisis exploratorio.
