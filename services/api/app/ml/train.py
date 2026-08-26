import json
import os

import joblib
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score

from app.ml.experiment_tracker import ExperimentTracker


MODEL_NAME = "compliance-risk-classifier"
MODEL_VERSION = "1.1.0"
DATA_DIR = "data/processed"
ARTIFACTS_DIR = "artifacts/compliance-risk-classifier"


def train_model():
    # ---------------------------------------------------------
    # Experiment tracking
    # ---------------------------------------------------------
    tracker = ExperimentTracker()

    tracker.set_tag("model_name", MODEL_NAME)
    tracker.set_tag("algorithm", "RandomForestClassifier")
    tracker.set_tag("model_version", MODEL_VERSION)

    # ---------------------------------------------------------
    # Load training and validation data
    # ---------------------------------------------------------
    train_path = os.path.join(DATA_DIR, "train.parquet")
    val_path = os.path.join(DATA_DIR, "val.parquet")

    train_df = pd.read_parquet(train_path)
    val_df = pd.read_parquet(val_path)

    X_train = train_df.drop(columns=["label", "finding_id"])
    y_train = train_df["label"]

    X_val = val_df.drop(columns=["label", "finding_id"])
    y_val = val_df["label"]

    # ---------------------------------------------------------
    # Feature definitions
    # ---------------------------------------------------------
    numeric_features = [
        "asset_criticality",
        "data_sensitivity",
        "historical_incidents",
        "business_impact",
        "regulatory_deadline_hours",
    ]

    categorical_features = [
        "framework",
        "requirement_type",
        "control_status",
        "evidence_status",
    ]

    text_feature = "finding_description"

    # ---------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                StandardScaler(),
                numeric_features,
            ),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features,
            ),
            (
                "text",
                TfidfVectorizer(max_features=500),
                text_feature,
            ),
        ]
    )

    # ---------------------------------------------------------
    # Model parameters
    # ---------------------------------------------------------
    params = {
        "n_estimators": 100,
        "random_state": 42,
        "class_weight": "balanced",
    }

    tracker.log_params(params)

    # ---------------------------------------------------------
    # Model pipeline
    # ---------------------------------------------------------
    model_pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor,
            ),
            (
                "classifier",
                RandomForestClassifier(**params),
            ),
        ]
    )

    # ---------------------------------------------------------
    # Train
    # ---------------------------------------------------------
    print("Training Random Forest compliance model...")

    model_pipeline.fit(
        X_train,
        y_train,
    )

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------
    predictions = model_pipeline.predict(X_val)

    macro_f1 = f1_score(
        y_val,
        predictions,
        average="macro",
        zero_division=0,
    )

    print(f"Validation Macro F1: {macro_f1:.4f}")

    print(
        classification_report(
            y_val,
            predictions,
            zero_division=0,
        )
    )

    # ---------------------------------------------------------
    # Track validation metrics
    # ---------------------------------------------------------
    tracker.log_metrics(
        {
            "validation_macro_f1": float(macro_f1),
        }
    )

    # ---------------------------------------------------------
    # Save artifacts
    # ---------------------------------------------------------
    os.makedirs(
        ARTIFACTS_DIR,
        exist_ok=True,
    )

    model_path = os.path.join(
        ARTIFACTS_DIR,
        "model.joblib",
    )

    joblib.dump(
        model_pipeline,
        model_path,
    )

    # ---------------------------------------------------------
    # Save metadata
    # ---------------------------------------------------------
    metadata = {
        "model_name": MODEL_NAME,
        "version": MODEL_VERSION,
        "framework": "sklearn",
        "task": "multiclass_classification",
        "classes": [
            "LOW",
            "MEDIUM",
            "HIGH",
            "CRITICAL",
        ],
        "parameters": params,
        "validation_macro_f1": float(macro_f1),
    }

    metadata_path = os.path.join(
        ARTIFACTS_DIR,
        "model_metadata.json",
    )

    with open(metadata_path, "w") as f:
        json.dump(
            metadata,
            f,
            indent=2,
        )

    # ---------------------------------------------------------
    # Finish experiment
    # ---------------------------------------------------------
    run_id = tracker.end_run("completed")

    print(f"Model artifacts saved to {ARTIFACTS_DIR}")

    print(f"Experiment run ID: {run_id}")

    return model_path


if __name__ == "__main__":
    train_model()
