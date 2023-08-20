from .base import BaseCRUD
from ..models.assist_models import MLModel
from ..schemas.ml_model_validations import MLModelCreate


class MLModelCRUD(BaseCRUD):

    def get_best_model(self, db):
        return db.query(self.model).filter_by(current_model=True).first()

    def create_or_update(self, db, model_data: MLModelCreate):
        existing_model = self.get(db, name=model_data.name)

        if existing_model:
            self.update(db, existing_model.id, **model_data.model_dump())
            self.get(db, id=existing_model.id)
        else:
            super().create(db, **model_data.model_dump())


ml_model_crud = MLModelCRUD(MLModel)
