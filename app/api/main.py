from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException

from app.api.schemas import (
    ChurnInput,
    ChurnPrediction,
    HealthResponse,
)


# ---------------------------------------------------------
# Configuración de rutas
# ---------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT_DIR / "models" / "churn_model.joblib"


# ---------------------------------------------------------
# Creación de la aplicación
# ---------------------------------------------------------

app = FastAPI(
    title="AndesLink Churn API",
    description=(
        "API local para estimar la probabilidad de abandono "
        "de clientes de AndesLink Servicios Digitales S.A."
    ),
    version="1.0.0",
)


# ---------------------------------------------------------
# Carga del modelo
# ---------------------------------------------------------

def load_model():
    """
    Carga el pipeline serializado desde la carpeta models.

    El pipeline contiene tanto el preprocesamiento como
    el modelo final seleccionado durante el entrenamiento.
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


# ---------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------

def determine_risk_level(probability: float) -> str:
    """
    Convierte la probabilidad de churn en una categoría
    descriptiva para facilitar la interpretación.
    """
    if probability >= 0.70:
        return "alto"

    if probability >= 0.40:
        return "medio"

    return "bajo"


# ---------------------------------------------------------
# Endpoints
# ---------------------------------------------------------

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

        return {
            "prediction": prediction,
            "churn_probability": round(probability, 4),
            "risk_level": determine_risk_level(probability),
            "model_name": "logistic_regression",
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"No se pudo generar la predicción: {error}",
        ) from error