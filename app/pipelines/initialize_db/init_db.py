from ...crud.training_data import training_data_crud
from ...db.session import SessionLocal
from ...services.training_models import naive_bayes
from datetime import datetime


def init_db():
    print('INIT DB TASK', datetime.now())
    db = SessionLocal()
    with open("data.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                sentence, action = line.split(" - ")
                training_data_crud.create(db=db, formal_sentence=sentence,
                                          predicted_action=action)
    naive_bayes(db)
