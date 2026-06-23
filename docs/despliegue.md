# Despliegue local de AndesLink Churn MLOps

## 1. Objetivo

Este documento describe cómo ejecutar localmente el sistema de predicción de churn desarrollado para AndesLink Servicios Digitales S.A.

La solución permite ingresar los datos de un cliente mediante una interfaz gráfica, enviarlos a una API de inferencia y obtener la clase predicha, la probabilidad estimada de churn, el nivel de riesgo y el nombre del modelo utilizado.

El modelo se carga desde `models/churn_model.joblib`, sin necesidad de reentrenarlo al iniciar la aplicación.

## 2. Arquitectura local

La solución está compuesta por:

- **Streamlit:** interfaz gráfica para ingresar datos y visualizar resultados.
- **FastAPI:** servicio de inferencia que valida los datos, ejecuta el modelo y devuelve la predicción.

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
Predicción y probabilidad
  |
  v
Resultado mostrado en Streamlit
```

Docker Compose construye y ejecuta ambos servicios dentro de una red local.

## 3. Requisitos

### Ejecución con Docker

- Docker Desktop.
- Docker Compose, incluido en Docker Desktop.
- Puertos `8000` y `8501` disponibles.

### Ejecución sin Docker

- Python 3.12.
- Un entorno virtual de Python.
- Dependencias declaradas en `requirements.txt`.

Todos los comandos deben ejecutarse desde la carpeta raíz del proyecto.

## 4. Ejecución con Docker Compose

Esta es la forma principal de despliegue.

### 4.1 Construir e iniciar los servicios

```powershell
docker compose up --build -d
```

Este comando construye la imagen, instala las dependencias e inicia FastAPI y Streamlit.

### 4.2 Verificar los contenedores

```powershell
docker compose ps
```

Los servicios `api` y `streamlit` deben aparecer en ejecución.

### 4.3 Accesos

- Swagger: `http://localhost:8000/docs`
- Estado de la API: `http://localhost:8000/health`
- Streamlit: `http://localhost:8501`

### 4.4 Consultar logs

```powershell
docker compose logs api
docker compose logs streamlit
```

Para seguir todos los logs en tiempo real:

```powershell
docker compose logs -f
```

### 4.5 Detener los servicios

```powershell
docker compose down
```

Este comando detiene y elimina los contenedores sin borrar el código ni el modelo.

## 5. Ejecución local sin Docker

### 5.1 Crear el entorno virtual

```powershell
python -m venv .venv
```

### 5.2 Instalar las dependencias

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 5.3 Iniciar FastAPI

En una primera terminal:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.api.main:app --reload
```

La API queda disponible en `http://localhost:8000` y Swagger en `http://localhost:8000/docs`.

### 5.4 Iniciar Streamlit

En una segunda terminal, manteniendo FastAPI activo:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app\streamlit_app\app.py
```

La interfaz queda disponible en `http://localhost:8501`.

## 6. Comunicación entre servicios

Sin Docker, Streamlit utiliza por defecto:

```text
http://127.0.0.1:8000
```

Con Docker Compose utiliza:

```text
http://api:8000
```

La dirección se configura mediante la variable de entorno `API_URL`. Dentro de Compose, `api` es el nombre del servicio de FastAPI y funciona como dirección interna entre contenedores.

## 7. Endpoints

### `GET /`

Devuelve información general de la aplicación.

### `GET /health`

Comprueba que la API esté activa y que el modelo haya sido cargado.

```json
{
  "status": "ok",
  "model_loaded": true
}
```

### `POST /predict`

Recibe los datos del cliente y devuelve la predicción de churn.

Ejemplo de solicitud:

```json
{
  "tenure_months": 7,
  "monthly_charge": 58.23,
  "total_charges": 326.5,
  "support_tickets": 2,
  "late_payments": 1,
  "avg_monthly_usage_gb": 81.83,
  "contract_type": "mensual",
  "payment_method": "transferencia",
  "internet_service": "cable",
  "has_streaming": 0,
  "has_security_pack": 1,
  "num_products": 3,
  "region": "centro",
  "customer_age": 53,
  "is_promo": 1
}
```

Ejemplo de respuesta:

```json
{
  "prediction": 1,
  "churn_probability": 0.6788,
  "risk_level": "medio",
  "model_name": "logistic_regression"
}
```

La probabilidad exacta depende de los datos enviados.

## 8. Validación y manejo de errores

El contrato de entrada y salida está definido con Pydantic. Se validan campos obligatorios, tipos, rangos numéricos, variables binarias y categorías permitidas.

Códigos principales:

- `200`: solicitud procesada correctamente.
- `422`: datos de entrada inválidos.
- `503`: modelo no disponible.
- `500`: error inesperado durante la inferencia.

Streamlit también informa errores de conexión, tiempo de espera o respuestas inválidas de la API.

## 9. Pruebas automáticas

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Las pruebas cubren el endpoint principal, el estado de la API, la carga del modelo, una predicción válida, el rechazo de datos inválidos y los componentes de datos y modelo del primer parcial.

La ejecución actual finaliza con **8 pruebas aprobadas**.

## 10. Evidencias de funcionamiento

Las evidencias se encuentran en [`reports/evidencias_segundo_parcial`](../reports/evidencias_segundo_parcial):

- `01_pytest_8_passed.png`
- `02_docker_compose_ps.png`
- `03_swagger_endpoints.png`
- `04_health_ok.png`
- `05_predict_ok.png`
- `06_streamlit_prediction.png`

Estas capturas muestran las pruebas aprobadas, los contenedores activos, los endpoints disponibles, las respuestas correctas de la API y la integración con Streamlit.
