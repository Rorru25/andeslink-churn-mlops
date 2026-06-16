# Arquitectura del primer parcial

El proyecto se organiza como una solución local de MLOps para clasificación binaria de churn. La arquitectura separa datos, notebooks, código fuente, modelos, pruebas y reportes para evitar una entrega basada únicamente en celdas manuales.

## Flujo

1. `data/raw/churn_sintetico.csv`: dataset original.
2. `notebooks/01_eda_churn.ipynb`: análisis exploratorio inicial.
3. `src/data.py`: carga y validación de datos.
4. `src/features.py`: preprocesamiento mediante `ColumnTransformer`.
5. `src/train.py`: entrenamiento, comparación de modelos, registro de métricas y serialización.
6. `src/evaluate.py`: evaluación independiente del modelo guardado.
7. `models/churn_model.joblib`: artefacto final listo para inferencia.
8. `reports/`: métricas, figuras e informe técnico.
9. `tests/`: pruebas mínimas de datos y modelo.

## Justificación

Esta organización permite trazabilidad, reproducibilidad y separación de responsabilidades, principios centrales de un flujo MLOps local.
