import json
from app.ml.artifact_manager import ArtifactManager

def register_model():
    metrics_path = "artifacts/compliance-risk-classifier/metrics.json"
    with open(metrics_path) as f:
        metrics = json.load(f)

    manager = ArtifactManager()
    manifest = manager.register(
        model_path="artifacts/compliance-risk-classifier/model.joblib",
        version="1.0.0",
        metrics={
            "accuracy": metrics["accuracy"],
            "macro_f1": metrics["macro_f1"],
            "weighted_f1": metrics["weighted_f1"],
            "high_recall": metrics["high_recall"],
            "critical_recall": metrics["critical_recall"],
        },
    )
    print(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    register_model()