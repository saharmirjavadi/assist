from .base import BaseCRUD
from ..models.assist_models import MLModelHistory
from sqlalchemy import func


class MLModelHistoryCRUD(BaseCRUD):

    def get_max_accuracy(self, db):
        return db.query(func.max(self.model.accuracy)).scalar()


ml_model_history_crud = MLModelHistoryCRUD(MLModelHistory)
