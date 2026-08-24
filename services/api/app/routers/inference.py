from fastapi import APIRouter

from app.inference.schemas import InferenceRequest, InferenceResponse
from app.inference.service import inference_service

router = APIRouter(prefix="/v1/inference", tags=["inference"])


@router.post("", response_model=InferenceResponse)
def run_inference(request: InferenceRequest):
    return inference_service.predict(request)
