# Datos Sinteticos de Ejemplo

Este directorio contiene archivos Excel con datos **ficticios** que replican
el esquema canonico de 36 columnas de los exports SISAV2, generados con un
random seed fijo. No contienen ningun dato real de VcM.

## Proposito

- Permitir ejecutar el pipeline sin acceso a los datos confidenciales reales.
- Servir como fixture de pruebas durante el desarrollo.
- Ejercitar las reglas de limpieza: los datos ficticios reproducen a proposito
  la suciedad observada en los datos reales (espacios y tabs incrustados, puntos
  finales en categorias, separadores multivalor, montos en 0, variantes de
  semestre), para que el pipeline se pruebe contra condiciones realistas.

## Convencion de nombres

Los archivos siguen el patron que parsea `src/ingest.py` (`parsear_nombre_archivo`):

```
NIVEL__convNN__descripcion.xlsx
```

Donde:
- `NIVEL`: nivel academico en mayusculas (ej. `PRE_GRADO`, `POST_GRADO`, `EXTENSION`)
- `__`: doble guion bajo como delimitador
- `convNN`: prefijo `conv` seguido del numero de convocatoria
- `descripcion`: texto libre con instrumento, semestre y año

Ejemplo: `PRE_GRADO__conv90__Convocatoria_EXTENSION_2024.xlsx`

## Generacion

Los archivos se generan con el script `data/sample/generar_sample.py`.
