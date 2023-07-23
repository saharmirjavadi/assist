from .api_base import APIBaseClass
from ..schemas.prediction_validation import PredictionRequest
from .data_processing import *
from ..db.dependency import get_db
from fastapi import Depends
from ..crud.base import BaseCRUD
from sqlalchemy.orm import Session
from .preparation_models import *
import os


class Assistant(APIBaseClass):
    def __init__(self):
        super().__init__()

        self.router.add_api_route('/assist/init', self.init_db, methods=['GET'])
        self.router.add_api_route('/assist/processing', self.prediction, methods=['POST'])
        self.router.add_api_route('/assist/dataset/update', self.store_training_data, methods=['GET'])
        self.router.add_api_route('/assist/reinforcement', self.reinforcement_model, methods=['GET'])

    async def prediction(self, prediction_request: PredictionRequest, db: Session = Depends(get_db)):
        sentence = prediction_request.sentence

        # Normalize the sentence
        normalizer_text = sentence_normalizer(sentence)

        # Tokenize the sentence
        tokenized_text = sentence_tokenizer(normalizer_text)

        # Transform the sentence into a vector
        text_vectorized = sentence_transformer(tokenized_text, db)

        # Predict the action for the sentence
        predicted_action, model_id = predict_sentence(text_vectorized)

        # Save user input
        self.store_user_input(normalizer_text, predicted_action, model_id)

        amount, number, operator = charge_pos_tagging(sentence)

        return {
            "predicted_action": predicted_action,
            "amount": amount,
            "number": number,
            "operator": operator
        }

    def init_db(self, db: Session = Depends(get_db)):
        with open("data.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    sentence, action = line.split(" - ")
                    base_crud = BaseCRUD(TrainingData)
                    base_crud.create(db=db, sentence=sentence,
                                     predicted_action=action)
        naive_bayes(db)

    def store_user_input(self, sentence, action, model_id):
        with open('user_input_log.txt', 'a', encoding='utf-8') as file:
            file.write(f"{sentence} - {action} - {model_id}\n")

    def reinforcement_model(self, db: Session = Depends(get_db)):
        naive_bayes(db)

    def store_training_data(self, db: Session = Depends(get_db)) -> None:
        file_path = 'user_input_log.txt'
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                sentence, action, model_id = line.strip().split(' - ')
                base_crud = BaseCRUD(TrainingData)
                training_data_obj = {'sentence': sentence,
                                     'predicted_action': action, 'model_id': model_id}
                base_crud.create(db=db, **training_data_obj)
        os.remove(file_path)
