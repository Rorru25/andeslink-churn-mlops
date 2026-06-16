import pandas as pd
from src.config import DATA_RAW_PATH, TARGET_COLUMN

REQUIRED_COLUMNS = [
    "tenure_months", "monthly_charge", "total_charges", "support_tickets",
    "late_payments", "avg_monthly_usage_gb", "contract_type",
    "payment_method", "internet_service", "has_streaming",
    "has_security_pack", "num_products", "region", "customer_age",
    "is_promo", "churn"
]

def load_raw_data(path=DATA_RAW_PATH) -> pd.DataFrame:
    """Carga el dataset crudo de churn."""
    return pd.read_csv(path)

def validate_data(df: pd.DataFrame) -> None:
    """Valida condiciones mínimas del dataset para evitar errores silenciosos."""
    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Faltan columnas obligatorias: {missing_columns}")
    if df.empty:
        raise ValueError("El dataset está vacío.")
    if df[TARGET_COLUMN].isna().any():
        raise ValueError("La variable objetivo contiene valores nulos.")
    if not set(df[TARGET_COLUMN].unique()).issubset({0, 1}):
        raise ValueError("La variable churn debe ser binaria: 0 o 1.")

def split_features_target(df: pd.DataFrame):
    """Separa variables predictoras y target."""
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]
    return X, y
