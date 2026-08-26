import os
import json
from app.ml.experiment_tracker import ExperimentTracker

def test_experiment_tracker_logs_run():
    tracker = ExperimentTracker()
    tracker.log_params({"learning_rate": 0.01})
    tracker.log_metrics({"accuracy": 0.92})
    tracker.set_tag("environment", "test")
    
    run_id = tracker.end_run("completed")
    run_file = os.path.join("artifacts/experiments", f"{run_id}.json")
    
    assert os.path.exists(run_file)
    with open(run_file) as f:
        data = json.load(f)
    
    assert data["parameters"]["learning_rate"] == 0.01
    assert data["metrics"]["accuracy"] == 0.92
    assert data["status"] == "completed"