import hashlib
from datetime import datetime, timezone
from typing import Dict, Any

class ECRIPGovernanceEngine:
    @staticmethod
    def generate_evidence_hash(document_content: bytes) -> str:
        """Generates a tamper-evident SHA-256 hash for audit evidence verification."""
        return hashlib.sha256(document_content).hexdigest()

    @staticmethod
    def format_ai_audit_record(
        model_name: str,
        prompt_version: str,
        response_text: str,
        confidence_score: float,
        user_id: str,
        tenant_id: str
    ) -> Dict[str, Any]:
        """Formats an immutable AI decision log for explainable compliance[cite: 4]."""
        response_hash = hashlib.sha256(response_text.encode('utf-8')).hexdigest()
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tenant_id": tenant_id,
            "user_id": user_id,
            "ai_metadata": {
                "model_name": model_name,
                "prompt_version": prompt_version,
                "response_hash": response_hash,
                "confidence_score": confidence_score
            },
            "retention_policy": "7_years_immutable"
        }