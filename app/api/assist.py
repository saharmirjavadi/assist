from .api_base import APIBaseClass
from .data_processing import *


class Assistant(APIBaseClass):
    def __init__(self):
        super().__init__()
        self.router.add_api_route(
            '/assist/processing', self.prediction, methods=['POST'])

    async def prediction(self, data: dict):
        sentence = data.get("sentence")

        # Normalize the sentence
        normalized_text = sentence_normalizer(sentence)

        # Tokenize the sentence
        tokenized_text = sentence_tokenizer(sentence)

        # Transform the sentence into a vector
        text_vectorized = sentence_transformer(tokenized_text)

        # Predict the action for the sentence
        predicted_action = predict_sentence(text_vectorized)

        return {"predicted_action": predicted_action}
