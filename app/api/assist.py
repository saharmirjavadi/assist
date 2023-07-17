from .api_base import APIBaseClass
from ..schemas.prediction_validation import PredictionRequest
from .data_processing import *


class Assistant(APIBaseClass):
    def __init__(self):
        super().__init__()
        self.router.add_api_route(
            '/assist/processing', self.prediction, methods=['POST'])

    async def prediction(self, prediction_request: PredictionRequest):

        sentence = prediction_request.sentence

        # Normalize the sentence
        normalizer_text = sentence_normalizer(sentence)

        # Tokenize the sentence
        tokenized_text = sentence_tokenizer(normalizer_text)

        # Transform the sentence into a vector
        text_vectorized = sentence_transformer(tokenized_text)

        # Predict the action for the sentence
        predicted_action = predict_sentence(text_vectorized)

        # if predicted_action == 'شارژ':

        amount, number, operator = charge_pos_tagging(sentence)
        return {
            "predicted_action": predicted_action,
            "amount": amount,
            "number": number,
            "operator": operator
        }

        # return {'status': 400, 'predicted_action': predicted_action}
