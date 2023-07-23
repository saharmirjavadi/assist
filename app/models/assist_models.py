from sqlalchemy import Column, Integer, LargeBinary, String, ForeignKey, Enum
from app.db.base_class import Base


class MLModel(Base):
    __tablename__ = 'ml_models'

    id = Column(Integer, primary_key=True, index=True)
    accuracy = Column(String)
    model_data = Column(LargeBinary)


class TrainingData(Base):
    __tablename__ = 'training_data'

    id = Column(Integer, primary_key=True)
    sentence = Column(String, nullable=False)
    predicted_action = Column(Enum('charge', 'internet', 'card_transfer', 'uncertain',
                                   name="action_types"), nullable=False)
    model_id = Column(Integer, ForeignKey(
        'ml_models.id', ondelete='CASCADE'), nullable=True)
