# SISAV2 Data Pipeline

Pipeline de ingenieria de datos que consolida y limpia las planillas de
iniciativas de Vinculacion con el Medio (VcM) exportadas desde SISAV2, hacia
una tabla analitica unica que alimenta un dashboard de gestion institucional.

## Problema que resuelve

Las iniciativas de VcM se registran en planillas Excel que varian en formato
segun el año y el instrumento. A lo largo del tiempo el formulario fue
cambiando: distinto numero de columnas, distintos nombres, distintas hojas, y
campos que aparecen o desaparecen entre convocatorias. Hacer reporteria sobre
esa fuente heterogenea, a mano, es lento y propenso a error.

Este pipeline absorbe esa heterogeneidad y entrega una tabla consolidada,
limpia y trazable, con las columnas-indicador que los graficos del dashboard
necesitan. El equipo de visualizacion consume un unico archivo en lugar de
lidiar con las planillas originales.

## Que hace

1. **Ingesta**: lee los Excel de cada convocatoria, valida su estructura y
   extrae metadatos (instrumento, año, convocatoria, semestre) del nombre del
   archivo.
2. **Consolidacion**: unifica las distintas familias de formato (2022-2025) en
   un esquema canonico de columnas-indicador, mapeando cada formato a un
   conjunto comun de campos.
3. **Limpieza**: aplica reglas documentadas (normalizacion de espacios y
   separadores, conversion de tipos, separacion de conceptos mezclados), cada
   una con un identificador estable.
4. **Auditoria**: registra cada modificacion atomica (que dato, valor original,
   valor resultante, regla aplicada, archivo de origen) para trazabilidad
   completa.
5. **Exportacion**: produce el consolidado en CSV y Parquet para consumo del
   equipo de visualizacion.

## Trazabilidad

El principio rector es que toda transformacion sea auditable. Si aparece un dato
sospechoso en el dashboard, debe poder rastrearse hasta su origen y conocerse
que regla lo modifico y por que. Cada regla de limpieza tiene un ID estable
(R-001, R-002, ...) presente en el codigo, en el audit log y en
`docs/reglas_transformacion.md`.

## Estructura del repositorio

```
sisav2-data-pipeline/
├── data/
│   ├── raw/        # Planillas reales (IGNORADO por Git, confidencial)
│   ├── sample/     # Datos sinteticos para correr sin datos reales
│   ├── staging/    # Capa intermedia (ignorada)
│   └── clean/      # Consolidado y audit log (ignorado; se regenera)
├── src/
│   ├── ingest.py       # Lectura de Excel y metadatos del nombre
│   ├── transform.py    # Reglas de limpieza (R-XXX)
│   ├── audit.py        # Modificacion-con-registro
│   ├── schema.py       # Esquema canonico
│   ├── profiling.py    # Perfilado de calidad
│   └── main.py         # Orquestador
├── notebooks/      # Exploracion, perfilado, validacion, consolidacion
├── docs/           # Diccionarios, reglas, alcance, mapeo de esquemas
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Notebooks

El analisis esta documentado de forma reproducible:

- `01_perfilado` - calidad de datos del formato base
- `02_comparacion_formatos` - formato legacy vs. expandido
- `03_exploracion_planillas_origen` - caracterizacion de las planillas fuente
- `04_consolidado_indicadores` - consolidacion y limpieza de las tres familias
- `05_validacion_y_resumen` - validacion final y resumen ejecutivo

Los notebooks se versionan **sin output** para no exponer datos reales en el
historial. Limpiar antes de comitear:

```bash
jupyter nbconvert --clear-output --inplace notebooks/*.ipynb
```

## Inicio rapido

Requisito: Python 3.11 o superior.

```bash
git clone https://github.com/altairBASIC/sisav2-data-pipeline.git
cd sisav2-data-pipeline

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Ejecutar sobre datos sinteticos de ejemplo
python -m src.main --input data/sample/ --output data/clean/
```

Para usar datos reales, colocar las planillas en `data/raw/` y cambiar
`--input`. Los datos reales nunca se versionan.

## Manejo de datos confidenciales

Las planillas reales son confidenciales y quedan fuera del control de versiones
via `.gitignore`. El repositorio incluye datos **sinteticos** (generados, no
derivados de datos reales) que replican el esquema y reproducen a proposito la
suciedad observada, para poder ejecutar y probar el pipeline sin acceso a la
fuente real.

## El consolidado

La salida principal es una tabla unica de iniciativas (2022-2025) con
columnas-indicador estandarizadas. Su documentacion de consumo - que columna es
que, cuales son multivalor y con que separador, desde que año hay datos - esta
en `docs/diccionario_consolidado.md`. Algunas columnas tienen cobertura parcial
por año: esto refleja como evoluciono el formulario de origen, no un error del
pipeline.

## Roadmap

- **Migrar la consolidacion a `src/`**: la logica de consolidacion vive hoy en
  notebook; migrarla a un modulo reproducible con pruebas.
- **Containerizacion OCI**: `Containerfile` compatible con Podman y Docker, con
  datos montados como volumen, nunca dentro de la imagen.
- **Conector a fuente en vivo**: adaptar la ingesta para leer desde una
  instancia de SISAV2 cuando este disponible, ademas de los Excel.

## Licencia

MIT - ver [LICENSE](LICENSE).
