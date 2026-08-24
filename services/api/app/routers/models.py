from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.models.schemas import Model, ModelCreate
from app.models.service import model_registry

router = APIRouter(prefix="/v1/models", tags=["models"])


@router.post("", response_model=Model, status_code=status.HTTP_201_CREATED)
def register_model(model_data: ModelCreate):
    return model_registry.register(model_data)


@router.get("", response_model=list[Model])
def list_models():
    return model_registry.list_models()


@router.get("/{model_id}", response_model=Model)
def get_model(model_id: UUID):
    model = model_registry.get(model_id)

    if model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found",
        )

    return model


@router.delete("/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_model(model_id: UUID):
    deleted = model_registry.delete(model_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found",
        )
