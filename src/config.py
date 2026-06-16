from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

DATA_RAW_PATH = ROOT_DIR / "data" / "raw" / "churn_sintetico.csv"
DATA_PROCESSED_PATH = ROOT_DIR / "data" / "processed" / "churn_processed.csv"

MODEL_DIR = ROOT_DIR / "models"
MODEL_PATH = MODEL_DIR / "churn_model.joblib"
METRICS_PATH = ROOT_DIR / "reports" / "evaluation_metrics.json"

REPORTS_DIR = ROOT_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

TARGET_COLUMN = "churn"
RANDOM_STATE = 42
TEST_SIZE = 0.20
