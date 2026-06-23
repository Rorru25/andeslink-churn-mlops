# AndesLink Churn MLOps

Proyecto académico desarrollado para la materia **Laboratorio de Minería de Datos** de ISTEA.

El objetivo es construir una solución local de Machine Learning para estimar la probabilidad de abandono de clientes (`churn`) de AndesLink Servicios Digitales S.A.

La entrega actual incluye entrenamiento y evaluación del modelo, serialización del pipeline, una API de inferencia, una interfaz gráfica, pruebas automáticas y despliegue local con Docker Compose. El monitoreo y la observabilidad se incorporarán en la etapa final.

## Objetivo analítico

Construir un modelo de clasificación binaria que estime si un cliente abandonará el servicio a partir de variables relacionadas con antigüedad, facturación, uso, soporte, pagos y características comerciales.

La variable objetivo es `churn`:

- `0`: el cliente permanece.
- `1`: el cliente abandona el servicio.

## Componentes implementados

- Análisis exploratorio y validación del dataset.
- Entrenamiento y comparación de modelos.
- Pipeline de preprocesamiento y clasificación.
- Registro de experimentos con MLflow.
- Definición del flujo de entrenamiento y evaluación en `dvc.yaml`.
- Modelo serializado con Joblib.
- API de inferencia desarrollada con FastAPI.
- Contrato de entrada y salida mediante Pydantic.
- Interfaz gráfica desarrollada con Streamlit.
- Pruebas automáticas con Pytest.
- Despliegue de FastAPI y Streamlit mediante Docker Compose.

## Arquitectura

```text
Usuario
  |
  v
Interfaz Streamlit
Puerto 8501
  |
  | POST /predict
  v
API FastAPI
Puerto 8000
  |
  | Validación con Pydantic
  v
Pipeline y modelo serializado
models/churn_model.joblib
  |
  v
Predicción y probabilidad de churn
  |
  v
Resultado mostrado en Streamlit
```

## Estructura principal

```text
andeslink-churn-mlops/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── schemas.py
│   └── streamlit_app/
│       ├── __init__.py
│       └── app.py
├── data/
│   └── raw/
│       └── churn_sintetico.csv
├── docs/
│   ├── arquitectura.md
│   └── despliegue.md
├── models/
│   └── churn_model.joblib
├── notebooks/
│   └── 01_eda_churn.ipynb
├── reports/
│   ├── evidencias_segundo_parcial/
│   ├── evaluation_metrics.json
│   ├── evaluation_report.json
│   └── informe_primer_parcial.md
├── src/
├── tests/
│   ├── test_api.py
│   ├── test_data.py
│   └── test_model.py
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── dvc.yaml
├── environment.yml
├── requirements.txt
└── README.md
```

## Dataset

Se utiliza el archivo `data/raw/churn_sintetico.csv`, proporcionado para el caso académico de AndesLink.

El dataset contiene 5000 registros y 16 columnas relacionadas con edad, antigüedad, facturación, consumo, productos contratados, soporte, pagos atrasados, tipo de contrato, método de pago, servicio de internet, región, servicios adicionales y la variable objetivo `churn`.

## Modelo seleccionado

Se compararon tres modelos:

- Logistic Regression.
- Random Forest.
- Gradient Boosting.

El modelo seleccionado fue **Logistic Regression**, utilizando el F1-score como principal criterio de comparación.

| Métrica | Resultado |
|---|---:|
| Accuracy | 0.723 |
| Precision | 0.621 |
| Recall | 0.476 |
| F1-score | 0.539 |
| ROC-AUC | 0.758 |

El pipeline final, que incluye preprocesamiento y modelo, se encuentra en:

```text
models/churn_model.joblib
```

## Ejecución con Docker Compose

Esta es la forma principal de levantar la solución completa.

### Requisitos

- Docker Desktop abierto.
- Docker Compose disponible.
- Puertos `8000` y `8501` libres.

Desde la raíz del proyecto:

```powershell
docker compose up --build -d
```

Verificar que los servicios estén activos:

```powershell
docker compose ps
```

Accesos:

- Swagger: `http://localhost:8000/docs`
- Estado de la API: `http://localhost:8000/health`
- Streamlit: `http://localhost:8501`

Para detener los servicios:

```powershell
docker compose down
```

La explicación técnica completa se encuentra en [`docs/despliegue.md`](docs/despliegue.md).

## Ejecución local sin Docker

### Crear un entorno virtual

```powershell
python -m venv .venv
```

### Instalar dependencias

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Iniciar FastAPI

En una primera terminal:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.api.main:app --reload
```

Swagger queda disponible en `http://localhost:8000/docs`.

### Iniciar Streamlit

Sin detener FastAPI, abrir una segunda terminal:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app\streamlit_app\app.py
```

La interfaz queda disponible en `http://localhost:8501`.

## Endpoints de la API

### `GET /`

Devuelve información general de la aplicación y las rutas disponibles.

### `GET /health`

Comprueba que la API esté activa y que el modelo haya sido cargado correctamente.

### `POST /predict`

Recibe los datos de un cliente y devuelve:

- clase predicha;
- probabilidad de churn;
- nivel de riesgo;
- nombre del modelo utilizado.

El contrato completo puede consultarse desde Swagger en `http://localhost:8000/docs`.

## Validación de funcionamiento

Con los servicios activos:

```powershell
Invoke-RestMethod http://localhost:8000/health
```

La respuesta esperada es:

```text
status       : ok
model_loaded : True
```

También puede verificarse una predicción desde `POST /predict` en Swagger o desde Streamlit.

## Pruebas automáticas

Para ejecutar todas las pruebas:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Las pruebas verifican:

- carga y estructura del dataset;
- funcionamiento del modelo;
- endpoint principal de la API;
- estado y carga del modelo;
- predicción con datos válidos;
- rechazo de datos inválidos.

La ejecución actual finaliza con **8 pruebas aprobadas**.

## Entrenamiento y evaluación

Para volver a ejecutar el entrenamiento:

```powershell
.\.venv\Scripts\python.exe -m src.train
```

Para evaluar el modelo guardado:

```powershell
.\.venv\Scripts\python.exe -m src.evaluate
```

Los resultados se almacenan en:

```text
reports/evaluation_metrics.json
reports/evaluation_report.json
```

## Seguimiento y reproducibilidad

El entrenamiento registra métricas y artefactos mediante MLflow.

```powershell
.\.venv\Scripts\python.exe -m mlflow ui --backend-store-uri sqlite:///mlflow.db
```

La interfaz queda disponible en `http://localhost:5000`.

El archivo `dvc.yaml` define las etapas de entrenamiento y evaluación.

## Evidencias del segundo parcial

Las capturas de funcionamiento se encuentran en [`reports/evidencias_segundo_parcial`](reports/evidencias_segundo_parcial) e incluyen:

- ejecución de Pytest;
- contenedores activos;
- endpoints de Swagger;
- respuesta de `GET /health`;
- respuesta de `POST /predict`;
- predicción mostrada en Streamlit.

## Documentos del proyecto

- [Arquitectura y flujo del primer parcial](docs/arquitectura.md)
- [Documento técnico del despliegue local](docs/despliegue.md)
- [Informe técnico del primer parcial](reports/informe_primer_parcial.md)

## Limitaciones y alcance actual

El proyecto utiliza el dataset proporcionado para el caso académico de AndesLink. Por lo tanto, los resultados no deben interpretarse como una validación sobre clientes reales.

El modelo obtuvo un recall de `0.476`, por lo que puede no identificar una parte de los clientes que efectivamente abandonarían el servicio. Las predicciones deben considerarse una herramienta de apoyo y no el único criterio para tomar decisiones comerciales.

La aplicación está diseñada para ejecutarse en un entorno local. Actualmente no incluye:

- autenticación ni control de acceso a la API;
- almacenamiento persistente de solicitudes y predicciones;
- monitoreo continuo del servicio y del modelo;
- detección de drift en los datos;
- despliegue en infraestructura productiva.

El monitoreo, la observabilidad y el análisis de drift se incorporarán en la etapa final del proyecto.
