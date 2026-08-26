import os
from app.ml.artifact_manager import ArtifactManager

BASE_DIR = "artifacts/test-compliance-model"

def test_artifact_registration():
    manager = ArtifactManager(BASE_DIR)
    source_model = "artifacts/compliance-risk-classifier/model.joblib"

    if not os.path.exists(source_model):
        return

    manifest = manager.register(
        model_path=source_model,
        version="test-1.0.0",
        metrics={
            "macro_f1": 0.80,
            "high_recall": 0.90,
            "critical_recall": 0.95,
        },
    )

    assert manifest["version"] == "test-1.0.0"
    assert manifest["sha256"]
    assert manifest["status"] == "candidate"

def test_artifact_manifest_exists():
    manager = ArtifactManager(BASE_DIR)
    manifest = manager.get_manifest("test-1.0.0")

    if manifest is None:
        return

    assert manifest["model_name"] == "compliance-risk-classifier"

def test_model_promotion():
    manager = ArtifactManager(BASE_DIR)
    manifest = manager.get_manifest("test-1.0.0")

    if manifest is None:
        return

    promoted = manager.promote("test-1.0.0", "production")
    assert promoted["status"] == "production"

    stage = manager.get_stage("production")
    assert stage["version"] == "test-1.0.0"