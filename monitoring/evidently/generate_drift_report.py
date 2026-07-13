from pathlib import Path

import pandas as pd
from evidently.metric_preset import DataDriftPreset, DataQualityPreset
from evidently.report import Report


ROOT_DIR = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = ROOT_DIR / "data" / "raw" / "churn_sintetico.csv"
PREDICTIONS_LOG_PATH = ROOT_DIR / "logs" / "predictions_log.csv"

REFERENCE_OUTPUT_PATH = ROOT_DIR / "data" / "reference" / "reference_data.csv"
CURRENT_OUTPUT_PATH = ROOT_DIR / "data" / "current" / "current_data.csv"
REPORT_OUTPUT_PATH = ROOT_DIR / "reports" / "monitoring" / "evidently_drift_report.html"


TARGET_COLUMN = "churn"

FEATURE_COLUMNS = [
    "customer_age",
    "tenure_months",
    "monthly_charge",
    "total_charges",
    "avg_monthly_usage_gb",
    "num_products",
    "has_streaming",
    "has_security_pack",
    "support_tickets",
    "late_payments",
    "contract_type",
    "payment_method",
    "internet_service",
    "region",
    "is_promo",
]


def load_reference_data() -> pd.DataFrame:
    """
    Carga el dataset original y toma las variables utilizadas por el modelo
    como datos de referencia.
    """
    data = pd.read_csv(RAW_DATA_PATH)

    reference_data = data[FEATURE_COLUMNS].copy()

    return reference_data


def load_current_data_from_logs() -> pd.DataFrame | None:
    """
    Carga datos actuales desde el log de inferencias generado por la API.

    El log guarda las columnas de entrada con prefijo input_.
    Para compararlas con el dataset de referencia, se renombra cada columna
    a su nombre original.
    """
    if not PREDICTIONS_LOG_PATH.exists():
        return None

    logs = pd.read_csv(PREDICTIONS_LOG_PATH)

    input_columns = [
        column
        for column in logs.columns
        if column.startswith("input_")
    ]

    if not input_columns:
        return None

    current_data = logs[input_columns].copy()

    current_data.columns = [
        column.replace("input_", "")
        for column in current_data.columns
    ]

    missing_columns = [
        column
        for column in FEATURE_COLUMNS
        if column not in current_data.columns
    ]

    if missing_columns:
        print(
            "El log de inferencias no contiene todas las columnas necesarias. "
            f"Columnas faltantes: {missing_columns}"
        )
        return None

    return current_data[FEATURE_COLUMNS].copy()


def build_simulated_current_data(reference_data: pd.DataFrame) -> pd.DataFrame:
    """
    Genera una ventana actual simulada a partir del dataset original.

    Esta alternativa permite generar el reporte aunque todavía no haya
    suficientes predicciones reales registradas en logs/predictions_log.csv.
    """
    current_data = reference_data.sample(
        n=min(500, len(reference_data)),
        random_state=42,
    ).copy()

    current_data["monthly_charge"] = current_data["monthly_charge"] * 1.15
    current_data["support_tickets"] = current_data["support_tickets"] + 1
    current_data["late_payments"] = current_data["late_payments"] + 1

    return current_data


def save_monitoring_datasets(
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
) -> None:
    """
    Guarda los datasets utilizados para monitoreo.
    """
    REFERENCE_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CURRENT_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    reference_data.to_csv(REFERENCE_OUTPUT_PATH, index=False)
    current_data.to_csv(CURRENT_OUTPUT_PATH, index=False)


def generate_report(
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
) -> None:
    """
    Genera un reporte HTML de calidad de datos y drift.
    """
    REPORT_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    report = Report(
        metrics=[
            DataQualityPreset(),
            DataDriftPreset(),
        ]
    )

    report.run(
        reference_data=reference_data,
        current_data=current_data,
    )

    report.save_html(str(REPORT_OUTPUT_PATH))


def main() -> None:
    reference_data = load_reference_data()

    current_data = load_current_data_from_logs()

    if current_data is None or len(current_data) < 20:
        print(
            "No hay suficientes inferencias registradas. "
            "Se usará una ventana actual simulada para generar el reporte."
        )
        current_data = build_simulated_current_data(reference_data)
    else:
        print(
            "Se usará logs/predictions_log.csv como ventana actual "
            "para el reporte de monitoreo."
        )

    save_monitoring_datasets(
        reference_data=reference_data,
        current_data=current_data,
    )

    generate_report(
        reference_data=reference_data,
        current_data=current_data,
    )

    print(f"Reporte generado en: {REPORT_OUTPUT_PATH}")


if __name__ == "__main__":
    main()