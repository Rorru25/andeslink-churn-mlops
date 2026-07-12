from prometheus_client import Counter, Gauge, Histogram


REQUEST_COUNT = Counter(
    "andeslink_api_requests_total",
    "Cantidad total de requests recibidos por la API",
    ["method", "endpoint", "http_status"],
)

REQUEST_LATENCY = Histogram(
    "andeslink_api_request_latency_seconds",
    "Tiempo de respuesta de la API en segundos",
    ["method", "endpoint"],
)

PREDICTIONS_TOTAL = Counter(
    "andeslink_predictions_total",
    "Cantidad total de predicciones generadas",
    ["prediction", "risk_level", "model_name"],
)

PREDICTION_PROBABILITY = Histogram(
    "andeslink_prediction_probability",
    "Distribución de probabilidades de churn generadas por el modelo",
)

PREDICTION_ERRORS_TOTAL = Counter(
    "andeslink_prediction_errors_total",
    "Cantidad total de errores ocurridos durante la inferencia",
)

MODEL_LOADED = Gauge(
    "andeslink_model_loaded",
    "Indica si el modelo fue cargado correctamente: 1 = sí, 0 = no",
)


def normalize_endpoint(path: str) -> str:
    """
    Agrupa rutas para evitar demasiadas etiquetas diferentes
    en las métricas de Prometheus.
    """
    known_paths = {
        "/": "/",
        "/health": "/health",
        "/predict": "/predict",
        "/metrics": "/metrics",
    }

    return known_paths.get(path, "other")