# Datos Sintéticos de Ejemplo

Este directorio contiene archivos Excel con datos **ficticios y anonimizados**
que replican el esquema de 36 columnas de los exports reales de SISAV2.

## Propósito

- Permitir ejecutar el pipeline sin acceso a datos confidenciales.
- Servir como fixture para pruebas durante desarrollo.
- Documentar implícitamente la convención de nombrado de archivos.

## Convención de nombres

Los archivos siguen el patrón (a confirmar con datos reales):

```
{instrumento}_{año}_{nro_convocatoria}_{semestre}.xlsx
```

Ejemplo: `ApS_2024_001_1S.xlsx`

## Generación

Los archivos se generan con el script `data/sample/generar_sample.py`.
