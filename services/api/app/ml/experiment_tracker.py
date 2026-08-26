import json
import os
import uuid
from datetime import datetime, timezone

class ExperimentTracker:
    def __init__(self, tracking_dir="artifacts/experiments"):
        self.tracking_dir = tracking_dir
        os.makedirs(self.tracking_dir, exist_ok=True)
        self.run_id = str(uuid.uuid4())
        self.run_data = {
            "run_id": self.run_id,
            "status": "running",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "parameters": {},
            "metrics": {},
            "tags": {}
        }

    def log_params(self, params: dict):
        self.run_data["parameters"].update(params)

    def log_metrics(self, metrics: dict):
        self.run_data["metrics"].update(metrics)

    def set_tag(self, key: str, value: str):
        self.run_data["tags"][key] = value

    def end_run(self, status="completed"):
        self.run_data["status"] = status
        self.run_data["finished_at"] = datetime.now(timezone.utc).isoformat()
        
        run_path = os.path.join(self.tracking_dir, f"{self.run_id}.json")
        with open(run_path, "w") as f:
            json.dump(self.run_data, f, indent=2)
        return self.run_id