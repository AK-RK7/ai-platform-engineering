import json
import hashlib
import shutil
from pathlib import Path
from datetime import datetime, timezone

class ArtifactManager:
    def __init__(self, base_dir="artifacts/compliance-risk-classifier"):
        self.base_dir = Path(base_dir)
        self.versions_dir = self.base_dir / "versions"
        self.versions_dir.mkdir(parents=True, exist_ok=True)

    def calculate_checksum(self, artifact_path):
        sha256 = hashlib.sha256()
        with open(artifact_path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def register(
        self,
        model_path,
        version,
        metrics,
        training_dataset="compliance_findings_v1",
        feature_version="1.0.0",
    ):
        source = Path(model_path)
        if not source.exists():
            raise FileNotFoundError(f"Model artifact not found: {source}")

        version_dir = self.versions_dir / version
        version_dir.mkdir(parents=True, exist_ok=True)

        destination = version_dir / "model.joblib"
        shutil.copy2(source, destination)

        checksum = self.calculate_checksum(destination)

        manifest = {
            "model_name": "compliance-risk-classifier",
            "version": version,
            "framework": "sklearn",
            "task": "multiclass_classification",
            "classes": ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
            "training_dataset": training_dataset,
            "feature_version": feature_version,
            "metrics": metrics,
            "artifact": "model.joblib",
            "sha256": checksum,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "candidate",
        }

        manifest_path = version_dir / "manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)

        return manifest

    def promote(self, version, stage="production"):
        version_dir = self.versions_dir / version
        if not version_dir.exists():
            raise FileNotFoundError(f"Version does not exist: {version}")

        manifest_path = version_dir / "manifest.json"
        with open(manifest_path) as f:
            manifest = json.load(f)

        manifest["status"] = stage
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)

        pointer = self.base_dir / f"{stage}.json"
        with open(pointer, "w") as f:
            json.dump(
                {
                    "model_name": "compliance-risk-classifier",
                    "version": version,
                    "stage": stage,
                },
                f,
                indent=2,
            )

        return manifest

    def get_stage(self, stage="production"):
        pointer = self.base_dir / f"{stage}.json"
        if not pointer.exists():
            return None
        with open(pointer) as f:
            return json.load(f)

    def get_manifest(self, version):
        path = self.versions_dir / version / "manifest.json"
        if not path.exists():
            return None
        with open(path) as f:
            return json.load(f)

    def list_versions(self):
        versions = []
        for directory in self.versions_dir.iterdir():
            if directory.is_dir():
                manifest = self.get_manifest(directory.name)
                if manifest:
                    versions.append(manifest)
        return sorted(
            versions,
            key=lambda item: item.get("created_at", ""),
            reverse=True,
        )