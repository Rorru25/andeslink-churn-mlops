# AndesLink Churn MLOps

Proyecto académico desarrollado para la materia **Laboratorio de Minería de Datos** de ISTEA.

El objetivo es construir una solución local de Machine Learning para estimar la probabilidad de abandono de clientes (`churn`) de AndesLink Servicios Digitales S.A.

El proyecto abarca actualmente:

* entrenamiento y evaluación del modelo;
* serialización del pipeline;
* exposición del modelo mediante una API;
* interfaz gráfica para realizar predicciones;
* pruebas automáticas;
* despliegue local con Docker Compose.

## Objetivo analítico

Construir un modelo de clasificación binaria que estime si un cliente abandonará el servicio a partir de variables relacionadas con antigüedad, facturación, uso, soporte, pagos y características comerciales.

La variable objetivo es `churn`:

* `0`: el cliente permanece;
* `1`: el cliente abandona el servicio.

## Componentes implementados

La solución incluye:

* análisis exploratorio del dataset;
* preparación y validación de datos;
* entrenamiento y comparación de modelos;
* pipeline de preprocesamiento y clasificación;
* registro de experimentos con MLflow;
* definición del flujo de entrenamiento y evaluación en `dvc.yaml`;
* modelo serializado con Joblib;
* API de inferencia desarrollada con FastAPI;
* contrato de entrada y salida mediante Pydantic;
* interfaz gráfica desarrollada con Streamlit;
* pruebas automáticas con Pytest;
* despliegue de FastAPI y Streamlit mediante Docker Compose.

## Arquitectura

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

## Estructura principal

andeslink-churn-mlops/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── schemas.py
│   └── streamlit_app/
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

## Dataset

Se utiliza el archivo `data/raw/churn_sintetico.csv`, proporcionado para el caso académico de AndesLink.

El dataset contiene 5000 registros y 16 columnas relacionadas con:

* edad y antigüedad del cliente;
* cargos mensuales y acumulados;
* consumo promedio;
* productos contratados;
* tickets de soporte;
* pagos atrasados;
* tipo de contrato;
* método de pago;
* servicio de internet;
* región;
* servicios adicionales;
* variable objetivo `churn`.

## Modelo seleccionado

Se compararon tres modelos:

* Logistic Regression;
* Random Forest;
* Gradient Boosting.

El modelo seleccionado fue **Logistic Regression**, utilizando el F1-score como principal criterio de comparación.

Resultados sobre el conjunto de prueba:

| Métrica   | Resultado |
| --------- | --------: |
| Accuracy  |     0.723 |
| Precision |     0.621 |
| Recall    |     0.476 |
| F1-score  |     0.539 |
| ROC-AUC   |     0.758 |

El pipeline final, que incluye preprocesamiento y modelo, se encuentra en:

models/churn_model.joblib

## Ejecución con Docker Compose

Esta es la forma principal de levantar la solución completa.

### Requisitos

* Docker Desktop abierto;
* Docker Compose disponible;
* puertos `8000` y `8501` libres.

Desde la raíz del proyecto:

docker compose up --build -d

Verificar que los servicios estén activos:

docker compose ps

Accesos:

* documentación Swagger: `http://localhost:8000/docs`
* estado de la API: `http://localhost:8000/health`
* interfaz Streamlit: `http://localhost:8501`

Para detener los servicios:

docker compose down

La explicación técnica completa se encuentra en [`docs/despliegue.md`](docs/despliegue.md).

## Ejecución local sin Docker

### Crear un entorno virtual

python -m venv .venv

### Instalar dependencias

.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

### Iniciar FastAPI

En una primera terminal:

.\.venv\Scripts\python.exe -m uvicorn app.api.main:app --reload

Swagger queda disponible en:

http://localhost:8000/docs

### Iniciar Streamlit

Sin detener FastAPI, abrir una segunda terminal:

.\.venv\Scripts\python.exe -m streamlit run app\streamlit_app\app.py

La interfaz queda disponible en:

http://localhost:8501

## Endpoints de la API

### `GET /`

Devuelve información general de la aplicación y las rutas disponibles.

### `GET /health`

Comprueba que la API esté activa y que el modelo haya sido cargado correctamente.

### `POST /predict`

Recibe los datos de un cliente y devuelve:

* clase predicha;
* probabilidad de churn;
* nivel de riesgo;
* nombre del modelo utilizado.

El contrato completo de entrada y salida puede consultarse desde Swagger:

http://localhost:8000/docs

## Validación de funcionamiento

Con los servicios activos, comprobar el estado de la API:

Invoke-RestMethod http://localhost:8000/health

La respuesta esperada es:

status : ok
model_loaded : True

También puede verificarse una predicción desde el endpoint `POST /predict` disponible en Swagger o desde la interfaz Streamlit.

## Pruebas automáticas

Para ejecutar todas las pruebas:

.\.venv\Scripts\python.exe -m pytest -v

Las pruebas verifican:

* carga y estructura del dataset;
* funcionamiento del modelo;
* endpoint principal de la API;
* estado y carga del modelo;
* predicción con datos válidos;
* rechazo de datos inválidos.

La ejecución debe finalizar con todas las pruebas aprobadas.

## Entrenamiento y evaluación

Para volver a ejecutar el entrenamiento:

.\.venv\Scripts\python.exe -m src.train

Para ejecutar la evaluación del modelo guardado:

.\.venv\Scripts\python.exe -m src.evaluate

Los resultados se almacenan en:

reports/evaluation_metrics.json
reports/evaluation_report.json

## Seguimiento de experimentos

El entrenamiento registra métricas y artefactos mediante MLflow.

Para abrir la interfaz local:

.\.venv\Scripts\python.exe -m mlflow ui --backend-store-uri sqlite:///mlflow.db

Luego acceder a:

http://localhost:5000

El archivo `dvc.yaml` define las etapas de entrenamiento y evaluación del proyecto.

## Documentos del proyecto

* [Arquitectura y flujo](docs/arquitectura.md)
* [Documento técnico del despliegue local](docs/despliegue.md)
* [Informe técnico ](reports/informe_primer_parcial.md)

## Limitaciones y alcance actual

El modelo seleccionado obtuvo un recall de `0.476`, lo que indica que todavía puede no identificar una parte de los clientes que efectivamente abandonarían el servicio. Por este motivo, las predicciones deben considerarse una herramienta de apoyo y no utilizarse como único criterio para tomar decisiones comerciales.

La aplicación está diseñada para ejecutarse en un entorno local. Actualmente no incluye:

* autenticación ni control de acceso a la API;
* almacenamiento persistente de las solicitudes y predicciones;
* monitoreo continuo del servicio y del modelo;
* detección de cambios o drift en los datos;
* despliegue en infraestructura productiva.

El monitoreo, la observabilidad y el análisis de drift se incorporarán en la etapa final del proyecto.
