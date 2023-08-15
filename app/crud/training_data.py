from .base import BaseCRUD
from ..models.assist_models import TrainingData


class TrainingDataCRUD(BaseCRUD):
    ...


training_data_crud = TrainingDataCRUD(TrainingData)
