from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ModelCreate(BaseModel):
    name: str = Field(min_length=1)
    version: str = Field(min_length=1)
    framework: str = Field(min_length=1)
    artifact_uri: str = Field(min_length=1)


class Model(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    version: str
    framework: str
    artifact_uri: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
