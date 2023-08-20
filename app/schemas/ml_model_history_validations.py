from pydantic import BaseModel


class MLModelHistoryCreate(BaseModel):
    name: str
    accuracy: str
    metrics: dict
