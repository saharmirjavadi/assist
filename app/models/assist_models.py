from sqlalchemy import Column, Integer, LargeBinary, String
from app.db.base_class import Base


class MLModel(Base):
    __tablename__ = "ml_models"

    id = Column(Integer, primary_key=True, index=True)
    accuracy = Column(String)
    model_data = Column(LargeBinary)
