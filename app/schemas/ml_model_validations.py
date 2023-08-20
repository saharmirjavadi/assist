from pydantic import BaseModel


class MLModelCreate(BaseModel):
    accuracy: str
    name: str
    trained_model: bytes
    current_model: bool
    metrics: dict