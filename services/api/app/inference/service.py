from uuid import uuid4

from fastapi import HTTPException

from app.inference.schemas import InferenceRequest, InferenceResponse
from app.models.service import model_registry


class InferenceService:
    def predict(self, request: InferenceRequest) -> InferenceResponse:
        model = model_registry.get(request.model_id)

        if model is None:
            raise HTTPException(
                status_code=404,
                detail="Model not found",
            )

        return InferenceResponse(
            model_id=model.id,
            model_name=model.name,
            model_version=model.version,
            prediction="positive",
            confidence=0.97,
            request_id=uuid4(),
        )


inference_service = InferenceService()
