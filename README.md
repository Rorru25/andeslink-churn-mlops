# AndesLink Churn MLOps

Proyecto académico para el primer parcial de Laboratorio de Minería de Datos. El objetivo es entrenar y documentar un modelo de Machine Learning para predecir abandono de clientes (`churn`) en una empresa simulada de suscripción mensual llamada AndesLink Servicios Digitales S.A.

## Objetivo analítico

Construir un modelo de clasificación binaria capaz de estimar si un cliente abandonará el servicio a partir de variables de antigüedad, facturación, comportamiento de uso, soporte, pagos y características comerciales.

## Estructura del proyecto

```text
andeslink-churn-mlops/
├─ data/raw/churn_sintetico.csv
├─ notebooks/01_eda_churn.ipynb
├─ src/
├─ models/
├─ reports/
├─ tests/
├─ docs/
├─ environment.yml
├─ requirements.txt
├─ dvc.yaml
└─ README.md
```

## Instalación

Con Conda:

```bash
conda env create -f environment.yml
conda activate andeslink-churn-mlops
```

O con pip:

```bash
pip install -r requirements.txt
```

## Entrenamiento

```bash
python -m src.train
```

El entrenamiento compara tres modelos:

- Logistic Regression
- Random Forest
- Gradient Boosting

El mejor modelo se selecciona según F1-score y se guarda en:

```text
models/churn_model.joblib
```

## Evaluación

```bash
python -m src.evaluate
```

Los resultados se guardan en:

```text
reports/evaluation_metrics.json
reports/evaluation_report.json
```

## MLflow

Si MLflow está instalado, el script de entrenamiento registra los experimentos automáticamente.

Para visualizar los experimentos:

```bash
mlflow ui
```

Luego abrir:

```text
http://localhost:5000
```

## Pruebas

```bash
pytest
```

## DVC

El archivo `dvc.yaml` documenta el pipeline reproducible de entrenamiento y evaluación.

```bash
dvc repro
```
