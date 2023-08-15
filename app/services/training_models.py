from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from hazm import word_tokenize, Normalizer
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from ..crud.ml_model import ml_model_crud
from ..crud.training_data import training_data_crud
from sklearn.pipeline import Pipeline
import joblib
import os


def naive_bayes(db):
    training_data = training_data_crud.get_all(db=db)
    texts = [item.formal_sentence for item in training_data]
    actions = [item.predicted_action for item in training_data]

    normalizer = Normalizer()
    sentences_normalized = [normalizer.normalize(sentence) for sentence in texts]
    sentences_tokenized = [word_tokenize(sentence) for sentence in sentences_normalized]
    normalized_sentences = [' '.join(tokens) for tokens in sentences_tokenized]

    pipeline = Pipeline([
        ('vectorizer', CountVectorizer()),
        ('classifier', MultinomialNB())
    ])

    X_train, X_test, y_train, y_test = train_test_split(normalized_sentences,
                                                        actions,
                                                        test_size=0.2,
                                                        random_state=42)

    # Train the pipeline
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    cls_report = {}
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average=None)

    for class_name, p, r, f in zip(pipeline.classes_, precision, recall, f1):
        class_metrics = {
            "Precision": p,
            "Recall": r,
            "F1-score": f
        }
        cls_report[class_name] = class_metrics

    with open(os.getcwd() + "/app/models/nb-model.joblib", "wb") as f:
        joblib.dump(pipeline, f)

    with open(os.getcwd()+"/app/models/nb-model.joblib", "rb") as f:
        serialized_model = f.read()

    max_model_accuracy = ml_model_crud.get_max_accuracy(db=db)
    max_accuracy = '0' if max_model_accuracy is None else max_model_accuracy
    current_model = True if str(accuracy) >= max_accuracy else False
    ml_model_crud.create(db=db, accuracy=accuracy,
                         model_data=serialized_model, current_model=current_model, metrics=cls_report)
    os.remove(os.getcwd()+"/app/models/nb-model.joblib")
