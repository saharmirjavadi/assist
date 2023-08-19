from .base import BaseCRUD
from ..models.assist_models import MLModel


class MLModelCRUD(BaseCRUD):

    def get_best_model(self, db):
        return db.query(self.model).filter_by(current_model=True).first()

    def create_or_update(self, db, **kwargs):
        existing_model = self.get(db, name=kwargs.get('name'))

        if existing_model:
            self.update(db, existing_model.id, **kwargs)
            new_model = self.get(db, id=existing_model.id)
        else:
            new_model = super().create(db, **kwargs)

        return new_model


ml_model_crud = MLModelCRUD(MLModel)
