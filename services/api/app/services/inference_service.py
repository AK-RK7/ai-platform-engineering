import json
import os
import uuid
import joblib
import pandas as pd

class InferenceService:
    def __init__(self):
        self.model = None
        self.model_version = None
        self.load_model()

    def load_model(self):
        pointer_path = "artifacts/compliance-risk-classifier/production.json"
        if not os.path.exists(pointer_path):
            self.model = None
            self.model_version = None
            return

        with open(pointer_path) as f:
            pointer = json.load(f)

        version = pointer["version"]
        model_path = f"artifacts/compliance-risk-classifier/versions/{version}/model.joblib"

        if not os.path.exists(model_path):
            raise FileNotFoundError(model_path)

        self.model = joblib.load(model_path)
        self.model_version = version

    def predict(self, model_id: str, payload: dict) -> dict:
        if self.model is None:
            self.load_model()

        if self.model is None:
            raise RuntimeError("No production ML model is available")

        df = pd.DataFrame([payload])
        prediction = self.model.predict(df)[0]
        probabilities = self.model.predict_proba(df)[0]
        confidence = float(max(probabilities))

        return {
            "model_id": model_id,
            "model_name": "compliance-risk-classifier",
            "model_version": self.model_version,
            "prediction": prediction,
            "confidence": confidence,
            "request_id": str(uuid.uuid4()),
        }

inference_service = InferenceService()