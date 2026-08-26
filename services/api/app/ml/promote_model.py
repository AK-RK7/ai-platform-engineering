from app.ml.artifact_manager import ArtifactManager

MIN_MACRO_F1 = 0.50
MIN_HIGH_RECALL = 0.50
MIN_CRITICAL_RECALL = 0.50

def promote_model(version="1.0.0"):
    manager = ArtifactManager()
    manifest = manager.get_manifest(version)

    if not manifest:
        raise RuntimeError(f"No manifest found for version {version}")

    metrics = manifest.get("metrics", {})
    macro_f1 = metrics.get("macro_f1", 0)
    high_recall = metrics.get("high_recall", 0)
    critical_recall = metrics.get("critical_recall", 0)

    if macro_f1 < MIN_MACRO_F1:
        raise RuntimeError(f"Macro F1 gate failed: {macro_f1:.4f}")
    if high_recall < MIN_HIGH_RECALL:
        raise RuntimeError(f"HIGH recall gate failed: {high_recall:.4f}")
    if critical_recall < MIN_CRITICAL_RECALL:
        raise RuntimeError(f"CRITICAL recall gate failed: {critical_recall:.4f}")

    promoted = manager.promote(version=version, stage="production")
    print(f"Model {version} promoted to production.")
    return promoted

if __name__ == "__main__":
    promote_model()