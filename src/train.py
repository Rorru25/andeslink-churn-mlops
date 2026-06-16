import json
from pathlib import Path

import joblib
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.config import METRICS_PATH, MODEL_DIR, MODEL_PATH, RANDOM_STATE, TEST_SIZE
from src.data import load_raw_data, split_features_target, validate_data
from src.features import build_preprocessor

try:
    import mlflow
    import mlflow.sklearn
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False


def evaluate_predictions(y_true, y_pred, y_proba):
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_true, y_proba),
    }


def train():
    df = load_raw_data()
    validate_data(df)
    X, y = split_features_target(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    models = {
        "logistic_regression": LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
        "random_forest": RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE),
        "gradient_boosting": GradientBoostingClassifier(random_state=RANDOM_STATE),
    }

    if MLFLOW_AVAILABLE:
        mlflow.set_experiment("andeslink_churn_training")

    results = {}
    best_name = None
    best_model = None
    best_f1 = -1

    for name, estimator in models.items():
        preprocessor = build_preprocessor(X_train)
        pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("model", estimator),
        ])

        if MLFLOW_AVAILABLE:
            run_context = mlflow.start_run(run_name=name)
        else:
            run_context = None

        try:
            pipeline.fit(X_train, y_train)
            y_pred = pipeline.predict(X_test)
            y_proba = pipeline.predict_proba(X_test)[:, 1]
            metrics = evaluate_predictions(y_test, y_pred, y_proba)
            results[name] = metrics

            if MLFLOW_AVAILABLE:
                for metric_name, metric_value in metrics.items():
                    mlflow.log_metric(metric_name, metric_value)
                mlflow.sklearn.log_model(pipeline, artifact_path="model")

            if metrics["f1"] > best_f1:
                best_f1 = metrics["f1"]
                best_name = name
                best_model = pipeline
        finally:
            if run_context is not None:
                mlflow.end_run()

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_model, MODEL_PATH)

    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    output = {
        "best_model": best_name,
        "selection_metric": "f1",
        "models": results,
    }
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

    print(f"Mejor modelo: {best_name}")
    print(json.dumps(output, indent=4))
    print(f"Modelo guardado en: {MODEL_PATH}")


if __name__ == "__main__":
    train()
