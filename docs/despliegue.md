# Despliegue local del proyecto AndesLink Churn

Este documento resume cómo levantar el proyecto en un entorno local y cómo comprobar que los servicios principales funcionan.

## Entorno utilizado

El proyecto fue probado localmente en Windows usando PowerShell, Docker Desktop y Python 3.12.

Para ejecutar el despliegue se necesita tener instalado:

- Python 3.12;
- Docker Desktop;
- Git;
- un editor como VS Code.

Todos los comandos se ejecutan desde la raíz del repositorio: andeslink-churn-mlops

## Dependencias locales

El proyecto usa un entorno virtual `.venv`.

Para instalar las dependencias:
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

En este trabajo no usé la activación tradicional del entorno virtual porque en PowerShell puede fallar por la política de ejecución de scripts. Por eso, los comandos llaman directamente al Python de `.venv`.

## Validación previa

Antes de levantar los servicios, se ejecutan las pruebas:

.\.venv\Scripts\python.exe -m pytest -v --disable-warnings

El despliegue se considera listo para probar si los tests pasan correctamente.

## Ejecución local de la API

Para probar solamente la API sin Docker:

.\.venv\Scripts\python.exe -m uvicorn app.api.main:app --reload

La API queda disponible en: http://127.0.0.1:8000

La documentación Swagger se puede abrir en: http://127.0.0.1:8000/docs

También se pueden revisar:

http://127.0.0.1:8000/health
http://127.0.0.1:8000/metrics

No se debe ejecutar directamente `app/api/main.py`, porque la API está preparada para iniciarse como módulo del proyecto.

## Despliegue con Docker Compose

Para levantar el sistema completo:

docker compose up --build -d

Para revisar el estado de los contenedores:

docker compose ps

Los servicios esperados son:

| Servicio               |Puerto| Uso               |
|------------------------|------|-------------------|
| `andeslink-api`        | 8000 | API de predicción |
| `andeslink-streamlit`  | 8501 | Interfaz web      |
| `andeslink-prometheus` | 9090 | Métricas          |
| `andeslink-grafana`    | 3000 | Dashboard         |

Si la API aparece como `healthy`, significa que el contenedor está respondiendo correctamente al endpoint `/health`.

## URLs principales

| Servicio   | URL                            |
|------------|--------------------------------|
| Swagger    | `http://localhost:8000/docs`   |
| Healthcheck| `http://localhost:8000/health` |
| Métricas   | `http://localhost:8000/metrics`|
| Streamlit  | `http://localhost:8501`        |
| Prometheus | `http://localhost:9090`        |
| Grafana    | `http://localhost:3000`        |

## Prueba de predicción

La predicción se puede probar desde Swagger o desde Streamlit.

Ejemplo de entrada para `/predict`:

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

Ejemplo de respuesta esperada:

```json
{
  "prediction": 1,
  "churn_probability": 0.6788,
  "risk_level": "medio",
  "model_name": "logistic_regression"
}
```

Cada predicción también genera un registro local en: logs/predictions_log.csv

Ese archivo no se versiona porque se genera durante la ejecución.

## Verificación de Prometheus

Prometheus se abre desde: http://localhost:9090

Para comprobar que está leyendo la API, se puede ejecutar esta consulta:

```promql
up{job="andeslink-api"}
```
El valor esperado es `1`.

También se pueden revisar métricas como:

```promql
andeslink_model_loaded
andeslink_api_requests_total
andeslink_predictions_total
```

Si todavía no se realizaron predicciones, algunas métricas pueden aparecer en cero o no tener valores suficientes.

## Verificación de Grafana

Grafana se abre desde: http://localhost:3000

Credenciales iniciales:

```text
Usuario: admin
Contraseña: musica15
```

El dashboard se encuentra en:

Dashboards > AndesLink > AndesLink API Monitoring

Para que los paneles tengan datos, conviene ejecutar algunas predicciones desde Swagger o Streamlit y esperar unos segundos a que Prometheus recolecte las métricas.

## Reporte de Evidently

El reporte de monitoreo de datos se genera con:

```powershell
.\.venv\Scripts\python.exe -m monitoring.evidently.generate_drift_report
```

El archivo generado queda en:

reports/monitoring/evidently_drift_report.html

Para abrirlo:

```powershell
Start-Process reports\monitoring\evidently_drift_report.html
```

Cuando todavía no hay suficientes inferencias reales registradas, el script usa una ventana actual simulada. Esto permite probar el flujo de monitoreo aunque el proyecto no tenga tráfico continuo.

## Apagar los servicios

Para detener los contenedores:

```powershell
docker compose down
```

Para volver a levantarlos:

```powershell
docker compose up --build -d
```

## Problemas encontrados

Durante el armado del despliegue aparecieron algunos problemas puntuales.

Uno fue una dependencia mal escrita en `requirements.txt`:

```text
httpxprometheus-client
```

La corrección fue separarla en dos líneas:

```text
httpx
prometheus-client
```

También apareció un error de codificación `UTF-8 BOM` al validar el JSON del dashboard de Grafana. Se resolvió guardando el archivo sin BOM.

Otro error posible es ejecutar directamente `app/api/main.py`. En ese caso puede aparecer:

```text
No module named app
```

La forma correcta de iniciar la API es:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.api.main:app --reload
```

## Comprobación final

Para dar por probado el despliegue, se revisa que:

- los tests pasen;
- `docker compose ps` muestre los cuatro servicios;
- Swagger responda;
- Streamlit permita consultar una predicción;
- `/health` indique que el modelo está cargado;
- `/metrics` exponga métricas;
- Prometheus muestre el job `andeslink-api` con valor `1`;
- Grafana cargue el dashboard;
- Evidently genere el reporte HTML.