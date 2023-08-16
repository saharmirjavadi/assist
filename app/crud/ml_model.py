from .base import BaseCRUD
from ..models.assist_models import MLModel


class MLModelCRUD(BaseCRUD):

    def get_best_model(self, db):
        return db.query(self.model).filter_by(current_model=True).first()

    def create_or_update(self, db, **kwargs):
        existing_model = self.get(db, name=kwargs['name'])

        if existing_model:
            existing_model.current_model = False
            db.commit()

            for key, value in kwargs.items():
                setattr(existing_model, key, value)

            new_model = existing_model
        else:
            new_model = super().create(db, **kwargs)

        return new_model


ml_model_crud = MLModelCRUD(MLModel)
