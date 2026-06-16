# AndesLink Churn MLOps

Proyecto académico correspondiente al primer parcial de **Laboratorio de Minería de Datos**. El objetivo es entrenar, evaluar y documentar un modelo de Machine Learning para predecir el abandono de clientes (*churn*) en AndesLink Servicios Digitales S.A., una empresa de suscripción mensual planteada como caso de trabajo.

## Objetivo analítico

Construir un modelo de clasificación binaria capaz de estimar si un cliente abandonará el servicio a partir de variables relacionadas con antigüedad, facturación, comportamiento de uso, soporte, pagos, tipo de contrato y características comerciales.

La variable objetivo es:

```text
churn
```

Donde:

```text
0 = cliente que permanece
1 = cliente que abandona
```

## Estructura del proyecto

```text
andeslink-churn-mlops/
├─ data/
│  └─ raw/
│     └─ churn_sintetico.csv
├─ notebooks/
│  └─ 01_eda_churn.ipynb
├─ src/
│  ├─ config.py
│  ├─ data.py
│  ├─ features.py
│  ├─ train.py
│  ├─ evaluate.py
│  ├─ predict.py
│  └─ utils.py
├─ models/
│  └─ churn_model.joblib
├─ reports/
│  ├─ evaluation_metrics.json
│  ├─ evaluation_report.json
│  └─ informe_primer_parcial.md
├─ tests/
│  ├─ test_data.py
│  └─ test_model.py
├─ docs/
│  └─ arquitectura.md
├─ environment.yml
├─ requirements.txt
├─ dvc.yaml
└─ README.md
```

## Instalación

### Opción 1: con Conda

```bash
conda env create -f environment.yml
conda activate andeslink-churn-mlops
```

### Opción 2: con entorno virtual y pip en Windows

Crear entorno virtual:

```powershell
python -m venv .venv
```

Instalar dependencias:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Entrenamiento

Para entrenar los modelos:

```bash
python -m src.train
```

En Windows, usando el entorno virtual local:

```powershell
.\.venv\Scripts\python.exe -m src.train
```

El entrenamiento compara tres modelos:

* Logistic Regression
* Random Forest Classifier
* Gradient Boosting Classifier

El mejor modelo se selecciona según F1-score y se guarda en:

```text
models/churn_model.joblib
```

## Evaluación

Para evaluar el modelo:

```bash
python -m src.evaluate
```

En Windows:

```powershell
.\.venv\Scripts\python.exe -m src.evaluate
```

Los resultados se guardan en:

```text
reports/evaluation_metrics.json
reports/evaluation_report.json
```

## MLflow

El script de entrenamiento registra los experimentos con MLflow.

Para visualizar los experimentos:

```bash
mlflow ui
```

Luego abrir en el navegador:

```text
http://localhost:5000
```

## Pruebas

Para ejecutar las pruebas:

```bash
pytest
```

En Windows:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Resultado esperado:

```text
4 passed
```

## DVC

El archivo `dvc.yaml` documenta el pipeline reproducible de entrenamiento y evaluación.

Para reproducir el flujo:

```bash
dvc repro
```

## Entregables del primer parcial

El repositorio incluye:

* dataset utilizado en `data/raw/`;
* notebook de análisis exploratorio en `notebooks/`;
* scripts reutilizables de carga, preparación, entrenamiento, evaluación y predicción en `src/`;
* modelo serializado en `models/churn_model.joblib`;
* métricas y reportes en `reports/`;
* informe técnico en `reports/informe_primer_parcial.md`;
* pruebas básicas en `tests/`;
* archivos de entorno reproducible: `environment.yml` y `requirements.txt`;
* documentación de arquitectura en `docs/arquitectura.md`;
* evidencia de tracking de experimentos con MLflow.

## Modelo seleccionado

El modelo seleccionado fue **Logistic Regression**, ya que obtuvo el mejor F1-score entre las alternativas evaluadas. El pipeline serializado incluye tanto el preprocesamiento como el modelo final, lo que permite reutilizarlo posteriormente para inferencia sin repetir manualmente las transformaciones.
