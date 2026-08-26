import os
from app.ml.artifact_manager import ArtifactManager
from app.ml.promotion_workflow import PromotionWorkflow

def test_promotion_workflow_gates():
    manager = ArtifactManager("artifacts/test-promotion-model")
    source_model = "artifacts/compliance-risk-classifier/model.joblib"
    
    if not os.path.exists(source_model):
        return

    # Register candidate model with passing metrics
    manager.register(
        model_path=source_model,
        version="workflow-1.0.0",
        metrics={
            "macro_f1": 0.85,
            "high_recall": 0.90,
            "critical_recall": 0.95
        }
    )

    workflow = PromotionWorkflow("artifacts/test-promotion-model")
    result = workflow.evaluate_and_promote("workflow-1.0.0", target_stage="production")
    
    assert result["status"] == "promoted"
    assert result["stage"] == "production"