from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from ..models.assist_models import TrainingData
from sklearn.naive_bayes import MultinomialNB
from ..models.assist_models import MLModel
from hazm import word_tokenize, Normalizer
from sklearn.metrics import accuracy_score
from ..crud.base import BaseCRUD
import joblib
import os


def naive_bayes(db):
    base_crud = BaseCRUD(TrainingData)

    training_data = base_crud.get_all(db=db)
    texts = [item.sentence for item in training_data]
    actions = [item.predicted_action for item in training_data]

    normalizer = Normalizer()
    sentences_normalized = [normalizer.normalize(sentence) for sentence in texts]
    sentences_tokenized = [word_tokenize(sentence) for sentence in sentences_normalized]
    normalized_sentences = [' '.join(tokens) for tokens in sentences_tokenized]

    vectorizer = CountVectorizer()
    X_vectorized = vectorizer.fit_transform(normalized_sentences)

    X_train, X_test, y_train, y_test = train_test_split(X_vectorized, 
                                                        actions, 
                                                        test_size=0.2, 
                                                        random_state=42)

    classifier = MultinomialNB()
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    with open(os.getcwd() + "/app/models/nb-model.joblib", "wb") as f:
        joblib.dump(classifier, f)

    with open(os.getcwd()+"/app/models/nb-model.joblib", "rb") as f:
        serialized_model = f.read()

    base_crud = BaseCRUD(MLModel)
    base_crud.create(db=db, accuracy=accuracy, model_data=serialized_model)