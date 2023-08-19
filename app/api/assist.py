from .api_base import APIBaseClass
from ..schemas.prediction_validation import PredictionRequest
from ..modules.pre_processing import *
from ..db.dependency import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from ..modules.training_models import *
from ..modules.prediction import prediction


class Assistant(APIBaseClass):
    def __init__(self):
        super().__init__()

        self.router.add_api_route(
            '/assist/processing', self.prediction, methods=['POST'])

    async def prediction(self, prediction_request: PredictionRequest, db: Session = Depends(get_db)):
        sentence = prediction_request.sentence
        return prediction(sentence, db)
