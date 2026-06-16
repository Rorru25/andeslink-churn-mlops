import json

import joblib
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split

from src.config import MODEL_PATH, RANDOM_STATE, REPORTS_DIR, TEST_SIZE
from src.data import load_raw_data, split_features_target


def evaluate():
    df = load_raw_data()
    X, y = split_features_target(df)

    _, X_test, _, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    model = joblib.load(MODEL_PATH)
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    results = {
        "classification_report": classification_report(y_test, y_pred, output_dict=True),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "roc_auc": roc_auc_score(y_test, y_proba),
    }

    output_path = REPORTS_DIR / "evaluation_report.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(json.dumps(results, indent=4))
    print(f"Reporte guardado en: {output_path}")


if __name__ == "__main__":
    evaluate()
