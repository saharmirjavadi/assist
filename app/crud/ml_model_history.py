from .base import BaseCRUD
from ..models.assist_models import MLModelHistory
from sqlalchemy import func
from ..schemas.ml_model_history_validations import MLModelHistoryCreate


class MLModelHistoryCRUD(BaseCRUD):

    def get_max_accuracy(self, db):
        return db.query(func.max(self.model.accuracy)).scalar()

    def create(self, db, model_history_data: MLModelHistoryCreate):
        return super().create(db, **model_history_data.model_dump())


ml_model_history_crud = MLModelHistoryCRUD(MLModelHistory)
