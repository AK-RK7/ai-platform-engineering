from uuid import UUID

from app.models.schemas import Model, ModelCreate


class ModelRegistry:
    def __init__(self):
        self._models: dict[UUID, Model] = {}

    def register(self, model_data: ModelCreate) -> Model:
        model = Model(**model_data.model_dump())
        self._models[model.id] = model
        return model

    def list_models(self) -> list[Model]:
        return list(self._models.values())

    def get(self, model_id: UUID) -> Model | None:
        return self._models.get(model_id)

    def delete(self, model_id: UUID) -> bool:
        return self._models.pop(model_id, None) is not None


model_registry = ModelRegistry()
