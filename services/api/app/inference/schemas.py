from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class InferenceRequest(BaseModel):
    model_id: UUID
    input: dict[str, Any]


class InferenceResponse(BaseModel):
    model_id: UUID
    model_name: str
    model_version: str
    prediction: str
    confidence: float
    request_id: UUID
