from hazm import word_tokenize, Normalizer
from ..crud.training_data import training_data_crud


def sentence_normalizer(sentence):
    normalizer = Normalizer()
    normalized_text = normalizer.normalize(sentence)
    return normalized_text


def sentence_tokenizer(sentence):
    tokenized_text = word_tokenize(sentence)
    normalized_text = ' '.join(tokenized_text)
    return normalized_text


def store_user_input(sentence, formal_sentence, action, model_id, db):
    training_data_obj = {'formal_sentence': formal_sentence, 'sentence': sentence,
                         'predicted_action': action, 'model_id': model_id}
    training_data_crud.create(db=db, **training_data_obj)
