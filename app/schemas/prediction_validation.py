from pydantic import BaseModel

class PredictionRequest(BaseModel):
    sentence: str

class PredictionResponse(BaseModel):
    predicted_action: str