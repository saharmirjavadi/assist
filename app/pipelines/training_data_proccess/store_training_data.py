from ...crud.base import BaseCRUD
from ...models.assist_models import TrainingData
from ...db.session import SessionLocal
import os
from datetime import datetime
from ...api.preparation_models import naive_bayes


def reinforcement_model() -> None:
    print('STORE TASK', datetime.now())
    db = SessionLocal()
    naive_bayes(db)
