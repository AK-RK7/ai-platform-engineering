import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.ml.generate_data import generate_compliance_dataset
from app.ml.train import train_model

client = TestClient(app)

def setup_module(module):
    generate_compliance_dataset(num_records=1500)
    train_model()

def test_model_artifact_exists():
    assert os.path.exists("artifacts/compliance-risk-classifier/model.joblib")
    assert os.path.exists("artifacts/compliance-risk-classifier/model_metadata.json")

def test_inference_endpoint_with_real_ml():
    payload = {
        "model_id": "3cd11a5e-b9d2-4df2-ac76-8767bfa3cddb",
        "inputs": {
            "framework": "GDPR",
            "requirement_type": "Security of Processing",
            "obligation_text": "Protect personal data",
            "control_description": "None",
            "finding_description": "Critical security breach and missing evidence.",
            "control_status": "NOT_IMPLEMENTED",
            "evidence_status": "MISSING",
            "asset_criticality": 5,
            "data_sensitivity": 5,
            "historical_incidents": 3,
            "business_impact": 5,
            "regulatory_deadline_hours": 72
        }
    }
    response = client.post("/v1/inference", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert data["prediction"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    assert "confidence" in data
    assert "request_id" in data