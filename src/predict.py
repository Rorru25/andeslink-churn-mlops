import joblib
import pandas as pd
from src.config import MODEL_PATH


def load_model():
    return joblib.load(MODEL_PATH)


def predict_churn(input_data: dict):
    model = load_model()
    df = pd.DataFrame([input_data])
    prediction = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[0][1])

    if probability >= 0.70:
        risk_label = "alto"
    elif probability >= 0.40:
        risk_label = "medio"
    else:
        risk_label = "bajo"

    return {
        "prediction": prediction,
        "churn_probability": probability,
        "risk_label": risk_label,
    }
