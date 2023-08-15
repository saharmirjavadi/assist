from .base import BaseCRUD
from ..models.assist_models import MLModel
from sqlalchemy import func


class MLModelCRUD(BaseCRUD):

    def get_max_accuracy(self, db):
        return db.query(func.max(self.model.accuracy)).scalar()

    def get_best_model(self, db):
        return db.query(self.model).filter_by(current_model=True).first()

    def create(self, db, current_model=False, **kwargs):
        if current_model:
            db.query(self.model).update({self.model.current_model: False})
        return super().create(db, current_model=current_model, **kwargs)


ml_model_crud = MLModelCRUD(MLModel)
