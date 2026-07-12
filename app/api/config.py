import os
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = Path(
    os.getenv(
        "MODEL_PATH",
        ROOT_DIR / "models" / "churn_model.joblib",
    )
)

MODEL_NAME = os.getenv("MODEL_NAME", "logistic_regression")
MODEL_VERSION = os.getenv("MODEL_VERSION", "1.0.0")

LOW_RISK_THRESHOLD = float(os.getenv("LOW_RISK_THRESHOLD", "0.40"))
HIGH_RISK_THRESHOLD = float(os.getenv("HIGH_RISK_THRESHOLD", "0.70"))

LOGS_DIR = Path(
    os.getenv(
        "LOGS_DIR",
        ROOT_DIR / "logs",
    )
)

PREDICTIONS_LOG_PATH = LOGS_DIR / "predictions_log.csv"