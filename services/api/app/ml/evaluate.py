import json
import os
import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

LABELS = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

def evaluate_model(
    model_path="artifacts/compliance-risk-classifier/model.joblib",
    test_path="data/processed/test.parquet",
):
    if not os.path.exists(model_path):
        raise FileNotFoundError(model_path)
    if not os.path.exists(test_path):
        raise FileNotFoundError(test_path)

    model = joblib.load(model_path)
    test_df = pd.read_parquet(test_path)

    X_test = test_df.drop(columns=["label", "finding_id"])
    y_test = test_df["label"]

    predictions = model.predict(X_test)
    report = classification_report(
        y_test, predictions, labels=LABELS, output_dict=True, zero_division=0
    )

    metrics = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "macro_f1": float(f1_score(y_test, predictions, average="macro", zero_division=0)),
        "weighted_f1": float(f1_score(y_test, predictions, average="weighted", zero_division=0)),
        "macro_precision": float(precision_score(y_test, predictions, average="macro", zero_division=0)),
        "macro_recall": float(recall_score(y_test, predictions, average="macro", zero_division=0)),
        "high_recall": float(report.get("HIGH", {}).get("recall", 0.0)),
        "critical_recall": float(report.get("CRITICAL", {}).get("recall", 0.0)),
        "classification_report": report,
        "confusion_matrix": confusion_matrix(y_test, predictions, labels=LABELS).tolist(),
        "labels": LABELS,
    }

    output_dir = os.path.dirname(model_path)
    with open(os.path.join(output_dir, "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"Test Macro F1: {metrics['macro_f1']:.4f}")
    print(f"HIGH Recall: {metrics['high_recall']:.4f}")
    print(f"CRITICAL Recall: {metrics['critical_recall']:.4f}")

    return metrics

if __name__ == "__main__":
    evaluate_model()