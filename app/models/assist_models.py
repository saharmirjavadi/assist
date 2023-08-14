from sqlalchemy import Column, Integer, LargeBinary, String, ForeignKey, Enum, Boolean, func, DateTime
from app.db.base_class import Base


class MLModel(Base):
    __tablename__ = 'ml_models'

    id = Column(Integer, primary_key=True, index=True)
    accuracy = Column(String)
    model_data = Column(LargeBinary)
    is_current_model = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())


class TrainingData(Base):
    __tablename__ = 'training_data'

    id = Column(Integer, primary_key=True)
    sentence = Column(String, nullable=False)
    predicted_action = Column(Enum('charge', 'internet', 'card_transfer', 'uncertain',
                                   name="action_types"), nullable=False)
    model_id = Column(Integer, ForeignKey(
        'ml_models.id', ondelete='CASCADE'), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
