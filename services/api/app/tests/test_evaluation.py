import os
from app.ml.evaluate import evaluate_model

def test_evaluation_generates_metrics():
    model_path = "artifacts/compliance-risk-classifier/model.joblib"
    test_path = "data/processed/test.parquet"

    if not os.path.exists(model_path) or not os.path.exists(test_path):
        return

    metrics = evaluate_model(model_path=model_path, test_path=test_path)
    assert "accuracy" in metrics
    assert "macro_f1" in metrics
    assert "weighted_f1" in metrics
    assert "high_recall" in metrics
    assert "critical_recall" in metrics
    assert "confusion_matrix" in metrics