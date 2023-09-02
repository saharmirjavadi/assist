
from .pre_processing import sentence_normalizer, sentence_tokenizer, store_user_input
from .pos_tagging import charge_pos_tagging, internet_pos_tagging
from ..crud.ml_model import ml_model_crud
from ..db.session import SessionLocal
from joblib import load
import io
import mlflow


def predict_sentence(tokenized_text):
    ml_model = ml_model_crud.get_best_model(db=SessionLocal())
    trained_model = ml_model.trained_model

    with io.BytesIO(trained_model) as f:
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
        action = "نامشخص"

    with mlflow.start_run():
        params = {
            "confidence_threshold": confidence_threshold,
        }
        mlflow.log_params(params)

        metrics = {
            "max_probability": max_proba,
        }
        mlflow.log_metrics(metrics)

        mlflow.sklearn.log_model(loaded_model, "model")

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

    if predicted_action == 'شارژ':
        amount, number, operator = charge_pos_tagging(sentence)
        return {
            "predicted_action": predicted_action,
            "amount": amount,
            "mobile": number,
            "operator_type": operator,
        }
    elif 'اینترنت':
        mobile, operator, package_value, volume, package_duration, phone_type = internet_pos_tagging(sentence)
        return {
            "predicted_action": predicted_action,
            "mobile": mobile,
            "operator_type": operator,
            "package": package_value,
            "package_volume": volume,
            "package_duration": package_duration,
            "type": phone_type,
        }
