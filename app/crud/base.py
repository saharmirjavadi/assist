from sqlalchemy.orm import Session
from sqlalchemy import func


class BaseCRUD:
    def __init__(self, model):
        self.model = model

    def get(self, db: Session, item_id: int):
        return db.query(self.model).filter(self.model.id == item_id).first()

    def create(self, db: Session, **kwargs):
        item = self.model(**kwargs)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    def delete(self, db: Session, item_id: int):
        item = db.query(self.model).filter(self.model.id == item_id).first()
        if item:
            db.delete(item)
            db.commit()
            return True
        return False

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def get_best_model(self, db: Session):
        return db.query(self.model).filter_by(is_current_model=True).first()

    def get_max_accuracy(self, db: Session):
        return db.query(func.max(self.model.accuracy)).scalar()
