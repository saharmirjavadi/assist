from ...crud.base import BaseCRUD
from ...models.assist_models import TrainingData
from ...db.session import SessionLocal
import os
from datetime import datetime
from ...api.preparation_models import naive_bayes



def reinforcement_model() -> None:
    print('STORE TASK', datetime.now())
    db = SessionLocal()
    file_path = 'user_input_log.txt'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                sentence, action, model_id = line.strip().split(' - ')
                base_crud = BaseCRUD(TrainingData)
                training_data_obj = {'sentence': sentence,
                                     'predicted_action': action, 'model_id': model_id}
                base_crud.create(db=db, **training_data_obj)
        os.remove(file_path)
        naive_bayes(db)
