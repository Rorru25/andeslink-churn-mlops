# AndesLink Churn MLOps

Proyecto académico de MLOps para predicción de abandono de clientes de AndesLink Servicios Digitales S.A.

El objetivo fue construir un flujo completo que incluya entrenamiento del modelo, despliegue mediante API, interfaz de consulta, contenedores y monitoreo básico del servicio y de los datos.

## Componentes principales

El proyecto incluye:

- modelo de clasificación para predicción de churn;
- API desarrollada con FastAPI;
- interfaz web en Streamlit;
- despliegue local con Docker Compose;
- métricas expuestas para Prometheus;
- dashboard en Grafana;
- reporte de drift con Evidently;
- pruebas automáticas con Pytest.

## Estructura del proyecto

```text
andeslink-churn-mlops/
├── app/
│   ├── api/
│   └── streamlit_app/
├── data/
├── docs/
├── models/
├── monitoring/
│   ├── evidently/
│   ├── grafana/
│   └── prometheus/
├── reports/
│   ├── evidencias_final/
│   └── monitoring/
├── src/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Ejecución local

Instalar dependencias:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Ejecutar pruebas:

```powershell
.\.venv\Scripts\python.exe -m pytest -v --disable-warnings
```

Levantar el sistema completo:

```powershell
docker compose up --build -d
```

Verificar servicios:

```powershell
docker compose ps
```

## Servicios disponibles

| Servicio | URL |
|---|---|
| Swagger | `http://localhost:8000/docs` |
| API health | `http://localhost:8000/health` |
| Métricas API | `http://localhost:8000/metrics` |
| Streamlit | `http://localhost:8501` |
| Prometheus | `http://localhost:9090` |
| Grafana | `http://localhost:3000` |

## Monitoreo

La API expone métricas en `/metrics`. Prometheus las recolecta y Grafana las muestra en un dashboard local.

También se generó un reporte de monitoreo de datos con Evidently:

```text
reports/monitoring/evidently_drift_report.html
```

El informe interpretado del monitoreo está en:

```text
reports/monitoring/informe_monitoreo.md
```

## Documentación

| Documento | Contenido |
|---|---|
| `docs/arquitectura.md` | Arquitectura general del sistema |
| `docs/despliegue.md` | Pasos para ejecutar y verificar el despliegue |
| `reports/monitoring/informe_monitoreo.md` | Interpretación del monitoreo y acciones correctivas |

## Evidencias finales

Las capturas de la ejecución final están en:

```text
reports/evidencias_final/
```

Incluyen pruebas, Docker Compose, predicción en Swagger, Prometheus, Grafana y Evidently.


## Limitaciones

El proyecto funciona como despliegue local para una entrega académica. No incluye despliegue cloud, autenticación, base de datos productiva, alertas automáticas ni reentrenamiento programado.