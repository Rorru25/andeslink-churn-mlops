# Despliegue local de AndesLink Churn MLOps

## 1. Objetivo

Este documento describe el despliegue local del sistema de predicción de churn desarrollado para AndesLink Servicios Digitales S.A.

La solución permite ingresar los datos de un cliente mediante una interfaz gráfica, enviarlos a una API de inferencia y obtener:

* la clase predicha;
* la probabilidad estimada de churn;
* el nivel de riesgo;
* el nombre del modelo utilizado.

El modelo se carga desde el archivo serializado `models/churn_model.joblib`. No es necesario volver a entrenarlo cada vez que se inicia la aplicación.

---

## 2. Arquitectura local

La solución está compuesta por dos servicios:

* **Streamlit:** interfaz gráfica utilizada para ingresar los datos del cliente y visualizar el resultado.
* **FastAPI:** servicio de inferencia que valida los datos, ejecuta el modelo y devuelve la predicción.

El flujo de la aplicación es el siguiente:

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

Docker Compose se utiliza para construir y ejecutar ambos servicios dentro de contenedores conectados mediante una red local.

---

## 3. Requisitos

### Para ejecutar el proyecto con Docker

* Docker Desktop.
* Docker Compose, incluido en Docker Desktop.
* Puertos locales `8000` y `8501` disponibles.

### Para ejecutarlo sin Docker

* Python 3.12.
* Un entorno virtual de Python.
* Las dependencias declaradas en `requirements.txt`.

Los comandos deben ejecutarse desde la carpeta raíz del proyecto.

---

## 4. Ejecución con Docker Compose

Esta es la forma principal de despliegue del proyecto.

### 4.1 Construir e iniciar los servicios

Con Docker Desktop abierto, ejecutar:

```powershell
docker compose up --build -d
```

Este comando:

* construye la imagen definida en el `Dockerfile`;
* instala las dependencias del proyecto;
* inicia el servicio de FastAPI;
* inicia la interfaz Streamlit;
* conecta ambos servicios mediante Docker Compose.

### 4.2 Verificar los contenedores

Ejecutar:

```powershell
docker compose ps
```

Los servicios `api` y `streamlit` deben aparecer en ejecución.

### 4.3 Acceder a las aplicaciones

Documentación Swagger de la API:

```text
http://localhost:8000/docs
```

Estado de la API:

```text
http://localhost:8000/health
```

Interfaz Streamlit:

```text
http://localhost:8501
```

### 4.4 Consultar los registros

Logs de FastAPI:

```powershell
docker compose logs api
```

Logs de Streamlit:

```powershell
docker compose logs streamlit
```

Para seguir los logs en tiempo real:

```powershell
docker compose logs -f
```

### 4.5 Detener los servicios

Ejecutar:

```powershell
docker compose down
```

Este comando detiene y elimina los contenedores creados por Docker Compose, sin borrar el código ni el modelo.

---

## 5. Ejecución local sin Docker

Esta alternativa puede utilizarse para desarrollo o verificación individual de los servicios.

### 5.1 Crear el entorno virtual

Desde la raíz del proyecto:

```powershell
python -m venv .venv
```

### 5.2 Instalar las dependencias

No es obligatorio activar el entorno virtual. Las dependencias pueden instalarse utilizando directamente su intérprete de Python:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 5.3 Iniciar FastAPI

En una primera terminal:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.api.main:app --reload
```

La API queda disponible en:

```text
http://localhost:8000
```

La documentación Swagger puede consultarse en:

```text
http://localhost:8000/docs
```

### 5.4 Iniciar Streamlit

Sin detener FastAPI, abrir una segunda terminal y ejecutar:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app\streamlit_app\app.py
```

La interfaz queda disponible en:

```text
http://localhost:8501
```

FastAPI debe permanecer en ejecución para que Streamlit pueda solicitar predicciones.

---

## 6. Comunicación entre los servicios

Cuando la aplicación se ejecuta localmente sin Docker, Streamlit utiliza por defecto:

```text
http://127.0.0.1:8000
```

Cuando se ejecuta mediante Docker Compose, utiliza:

```text
http://api:8000
```

La dirección de la API se configura mediante la variable de entorno `API_URL` definida en `docker-compose.yml`.

Dentro de Docker Compose, `api` es el nombre del servicio de FastAPI y funciona como dirección interna entre los contenedores.

---

## 7. Endpoints disponibles

### `GET /`

Devuelve información general de la aplicación y las rutas disponibles.

### `GET /health`

Comprueba que la API esté activa y que el modelo haya sido cargado.

Ejemplo de respuesta:

```json
{
  "status": "ok",
  "model_loaded": true
}
```

### `POST /predict`

Recibe los datos de un cliente y devuelve la predicción de churn.

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

El valor exacto de la probabilidad depende de los datos enviados.

---

## 8. Validación y manejo de errores

El contrato de entrada y salida de la API está definido mediante modelos Pydantic.

Entre las validaciones implementadas se incluyen:

* campos obligatorios;
* tipos de datos numéricos y categóricos;
* edad dentro del rango permitido;
* valores numéricos no negativos;
* variables binarias limitadas a `0` y `1`;
* categorías permitidas para contrato, región, método de pago y servicio de internet.

La API puede devolver los siguientes códigos:

* `200`: solicitud procesada correctamente;
* `422`: datos de entrada inválidos;
* `503`: el modelo no está disponible;
* `500`: error inesperado durante la inferencia.

La interfaz Streamlit también muestra mensajes cuando no puede conectarse con la API o cuando la solicitud no se procesa correctamente.

---

## 9. Pruebas automáticas

Las pruebas se ejecutan con Pytest.

Desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Las pruebas verifican:

* el funcionamiento del endpoint principal;
* el estado de la API;
* la carga del modelo;
* una predicción con datos válidos;
* el rechazo de datos inválidos;
* los componentes de datos y modelo desarrollados anteriormente.

La ejecución debe finalizar con todas las pruebas aprobadas.

---

## 10. Evidencias de funcionamiento

Para demostrar el funcionamiento local de la solución se deben incluir capturas o registros de:

* Swagger mostrando los endpoints disponibles;
* respuesta correcta de `GET /health`;
* respuesta correcta de `POST /predict`;
* interfaz Streamlit mostrando una predicción;
* resultado de `docker compose ps`;
* ejecución de Pytest con las pruebas aprobadas.

Estas evidencias permiten comprobar que la API, la interfaz, el modelo y los contenedores funcionan de manera integrada.
