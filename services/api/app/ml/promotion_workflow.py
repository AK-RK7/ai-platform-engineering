import json
import os
from app.ml.artifact_manager import ArtifactManager

class PromotionWorkflow:
    def __init__(self, base_dir="artifacts/compliance-risk-classifier"):
        self.artifact_manager = ArtifactManager(base_dir)
        self.thresholds = {
            "macro_f1": 0.70,
            "high_recall": 0.80,
            "critical_recall": 0.80
        }

    def evaluate_and_promote(self, version: str, target_stage="production"):
        manifest = self.artifact_manager.get_manifest(version)
        if not manifest:
            raise ValueError(f"Model version {version} not found.")

        metrics = manifest.get("metrics", {})
        
        # Check against promotion thresholds
        for metric, threshold in self.thresholds.items():
            val = metrics.get(metric, 0.0)
            if val < threshold:
                return {
                    "status": "rejected",
                    "reason": f"Gate failed for {metric}: {val} < threshold {threshold}",
                    "version": version
                }

        # Promote model if all gates pass
        promoted_manifest = self.artifact_manager.promote(version, stage=target_stage)
        return {
            "status": "promoted",
            "stage": target_stage,
            "version": version,
            "manifest": promoted_manifest
        }