from sqlalchemy import Column, LargeBinary, String, ForeignKey, Enum, Boolean, DateTime, UUID, func
from app.db.base_class import Base
import uuid


class MLModel(Base):
    __tablename__ = 'ml_models'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    accuracy = Column(String)
    model_data = Column(LargeBinary)
    current_model = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())


class TrainingData(Base):
    __tablename__ = 'training_data'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sentence = Column(String, nullable=True)
    formal_sentence = Column(String, nullable=False)
    model_id = Column(UUID, ForeignKey('ml_models.id', ondelete='CASCADE'), nullable=True)
    predicted_action = Column(Enum('charge', 'internet', 'card_transfer', 'uncertain', name="action_types"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
