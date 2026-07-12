import csv
from datetime import datetime, timezone

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException

from app.api.config import (
    
    HIGH_RISK_THRESHOLD,
    LOGS_DIR,
    LOW_RISK_THRESHOLD,
    MODEL_NAME,
    MODEL_PATH,
    MODEL_VERSION,
    PREDICTIONS_LOG_PATH,
)
from app.api.schemas import (
    ChurnInput,
    ChurnPrediction,
    HealthResponse,
)


app = FastAPI(
    title="AndesLink Churn API",
    description=(
        "API local para estimar la probabilidad de abandono "
        "de clientes de AndesLink Servicios Digitales S.A."
    ),
    version="1.0.0",
)


def load_model():
    """
    Carga el pipeline serializado desde la carpeta models.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró el modelo en: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


try:
    model = load_model()
    model_loaded = True
except Exception as error:
    model = None
    model_loaded = False
    model_load_error = str(error)


def determine_risk_level(probability: float) -> str:
    """
    Convierte la probabilidad de churn en una categoría
    descriptiva para facilitar la interpretación.
    """
    if probability >= HIGH_RISK_THRESHOLD:
        return "alto"

    if probability >= LOW_RISK_THRESHOLD:
        return "medio"

    return "bajo"


def write_prediction_log(
    customer_data: dict,
    prediction: int,
    probability: float,
    risk_level: str,
) -> None:
    """
    Registra cada inferencia en un archivo CSV local.

    Este log permite contar con una base simple para análisis posterior,
    monitoreo de predicciones y generación de reportes de drift.
    """
    try:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

        file_exists = PREDICTIONS_LOG_PATH.exists()

        row = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "model_name": MODEL_NAME,
            "model_version": MODEL_VERSION,
            "prediction": prediction,
            "churn_probability": round(probability, 4),
            "risk_level": risk_level,
        }

        for key, value in customer_data.items():
            row[f"input_{key}"] = value

        with PREDICTIONS_LOG_PATH.open(
            mode="a",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=list(row.keys()),
            )

            if not file_exists:
                writer.writeheader()

            writer.writerow(row)

    except Exception as error:
        print(f"No se pudo registrar la inferencia: {error}")


@app.get("/")
def root():
    """
    Endpoint inicial de la API.
    """
    return {
        "application": "AndesLink Churn API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "/health",
        "prediction": "/predict",
    }


@app.get(
    "/health",
    response_model=HealthResponse,
)
def health():
    """
    Informa si la API se encuentra disponible
    y si el modelo fue cargado correctamente.
    """
    return {
        "status": "ok" if model_loaded else "error",
        "model_loaded": model_loaded,
    }


@app.post(
    "/predict",
    response_model=ChurnPrediction,
)
def predict_churn(customer: ChurnInput):
    """
    Recibe los datos de un cliente y devuelve:

    - clase predicha;
    - probabilidad de churn;
    - nivel de riesgo;
    - modelo utilizado.
    """
    if model is None:
        detail = globals().get(
            "model_load_error",
            "El modelo no pudo cargarse.",
        )

        raise HTTPException(
            status_code=503,
            detail=f"Modelo no disponible: {detail}",
        )

    try:
        if hasattr(customer, "model_dump"):
            customer_data = customer.model_dump()
        else:
            customer_data = customer.dict()

        input_dataframe = pd.DataFrame([customer_data])

        prediction = int(model.predict(input_dataframe)[0])
        probability = float(
            model.predict_proba(input_dataframe)[0][1]
        )
        risk_level = determine_risk_level(probability)

        write_prediction_log(
            customer_data=customer_data,
            prediction=prediction,
            probability=probability,
            risk_level=risk_level,
        )

        return {
            "prediction": prediction,
            "churn_probability": round(probability, 4),
            "risk_level": risk_level,
            "model_name": MODEL_NAME,
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"No se pudo generar la predicción: {error}",
        ) from error