
from .pos_tagging import charge_pos_tagging
from .pre_processing import sentence_normalizer, sentence_tokenizer, store_user_input
from .pos_tagging import charge_pos_tagging, internet_pos_tagging
from ..crud.ml_model import ml_model_crud
from ..db.session import SessionLocal
from joblib import load
import io


def predict_sentence(tokenized_text):
    ml_model = ml_model_crud.get_best_model(db=SessionLocal())
    serialized_model = ml_model.model_data

    with io.BytesIO(serialized_model) as f:
        loaded_pipeline = load(f)

    loaded_model = loaded_pipeline.named_steps['classifier']
    vectorizer = loaded_pipeline.named_steps['vectorizer']

    text_vectorized = vectorizer.transform([tokenized_text])

    predicted_proba = loaded_model.predict_proba(text_vectorized)
    max_proba = max(predicted_proba[0])

    confidence_threshold = 0.9

    if max_proba >= confidence_threshold:
        predicted_label_index = predicted_proba.argmax()
        action = loaded_model.classes_[predicted_label_index]
    else:
        action = "uncertain"

    return action, ml_model.id


def prediction(sentence, db):
    # Normalize the sentence
    normalizer_text = sentence_normalizer(sentence)

    # Tokenize the sentence
    tokenized_text = sentence_tokenizer(normalizer_text)

    # Predict the action for the sentence
    predicted_action, model_id = predict_sentence(tokenized_text)

    # Save user input
    store_user_input(sentence, normalizer_text, predicted_action, model_id, db)

    if predicted_action == 'charge':
        amount, number, operator = charge_pos_tagging(sentence)
        return {
            "predicted_action": predicted_action,
            "amount": amount,
            "number": number,
            "operator": operator
        }
    elif 'internet':
        mobile, operator, package, package_duration = internet_pos_tagging(sentence)
        return {
            "predicted_action": predicted_action,
            "number": mobile,
            "operator": operator,
            "package": package,
            "package_duration": package_duration
        }
