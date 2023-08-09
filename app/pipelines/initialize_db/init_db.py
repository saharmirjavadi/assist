from ...crud.base import BaseCRUD
from ...models.assist_models import TrainingData
from ...db.session import SessionLocal
from ...api.preparation_models import naive_bayes
from datetime import datetime


def init_db():
    print('INIT DB TASK', datetime.now())
    db = SessionLocal()
    with open("data.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                sentence, action = line.split(" - ")
                base_crud = BaseCRUD(TrainingData)
                base_crud.create(db=db, sentence=sentence,
                                 predicted_action=action)
    naive_bayes(db)
