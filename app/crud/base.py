from sqlalchemy.orm import Session


class BaseCRUD:
    def __init__(self, model):
        self.model = model

    def get(self, db: Session, **kwargs):
        return db.query(self.model).filter_by(**kwargs).first()

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

    def update(self, db: Session, item_id: int, **kwargs):
        item = self.get(db, id=item_id)
        if item:
            for key, value in kwargs.items():
                setattr(item, key, value)
            db.commit()
            return True
        return False