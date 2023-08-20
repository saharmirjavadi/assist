from ..db.session import SessionLocal
from datetime import datetime
from ..modules.training_models import naive_bayes


def reinforcement_model() -> None:
    print('STORE TASK', datetime.now())
    db = SessionLocal()
    naive_bayes(db)
