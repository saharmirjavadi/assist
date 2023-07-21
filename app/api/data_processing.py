from sklearn.feature_extraction.text import CountVectorizer
from hazm import word_tokenize, Normalizer, InformalNormalizer, POSTagger
from persian_tools import phone_number, digits
from .phone_operator import get_phone_operator
from persian import convert_fa_numbers
from ..schemas.phone_number_validation import PhoneNumber
from ..crud.base import BaseCRUD
from ..models.assist_models import MLModel
from ..db.session import SessionLocal
from joblib import load
import difflib
import re
import os
import io


def load_data():
    dataset = []
    with open("data.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                sentence, action = line.split(" - ")
                dataset.append(sentence)
    return dataset


def sentence_normalizer(sentence):
    normalizer = Normalizer()
    normalized_text = normalizer.normalize(sentence)
    return normalized_text


def sentence_tokenizer(sentence):
    tokenized_text = word_tokenize(sentence)
    normalized_text = ' '.join(tokenized_text)
    return normalized_text


def sentence_transformer(normalized_text):
    vectorizer = CountVectorizer()
    vectorizer.fit_transform(load_data())
    text_vectorized = vectorizer.transform([normalized_text])
    return text_vectorized


def predict_sentence(text_vectorized):
    base_crud = BaseCRUD(MLModel)
    ml_model = base_crud.get(db=SessionLocal(), item_id=1)
    serialized_model = ml_model.model_data
    with io.BytesIO(serialized_model) as f:
        loaded_model = load(f)

    print('***', loaded_model)
    predicted_proba = loaded_model.predict_proba(text_vectorized)
    max_proba = max(predicted_proba[0])

    confidence_threshold = 0.9

    if max_proba >= confidence_threshold:
        predicted_label_index = predicted_proba.argmax()
        action = loaded_model.classes_[predicted_label_index]
    else:
        action = "داداش داری اشتباه میزنی"

    return action


def charge_pos_tagging(sentence):
    tagger = POSTagger(model=os.getcwd()+'/app/models/pos_tagger.model')
    normalized_sentence = InformalNormalizer(decrease_repeated_chars=True,
                                             correct_spacing=True,
                                             remove_specials_chars=True,
                                             persian_style=True).normalize(sentence)
    normalized_sentence = [''.join(ele) for ele in normalized_sentence[0]]
    normalized_sentence = " ".join(normalized_sentence)

    tokenized_sentence = word_tokenize(normalized_sentence)
    if 'یک' in tokenized_sentence:
        if tokenized_sentence[tokenized_sentence.index('یک') + 1] == 'شارژ':
            tokenized_sentence.remove('یک')

    tagged_sentence = tagger.tag(tokenized_sentence)
    # print(tagged_sentence)
    # print(tagger.data_maker(tokens=tagged_sentence))

    amount = 1
    mobile = None
    operator = None
    currency_symbol = 'ریال'
    operators = ["ایرانسل", "همراه اول", "رایتل"]

    for word, tag in tagged_sentence:
        # print(tag, word)
        if tag == 'VERB':
            tokenized_sentence.remove(word)

        if tag == 'NUM':
            number = convert_fa_numbers(word)
            if phone_number.validate(number):
                tokenized_sentence.remove(word)
                mobile = number

        for keyword in operators:
            similarity_score = difflib.SequenceMatcher(
                None, keyword, word).ratio()
            if similarity_score >= 0.8:
                operator = keyword

    normalized_text = ' '.join(tokenized_sentence)

    pattern = r'(\d+(\s+\w+)*)\s+(تومان|ریال|ت)'
    match = re.search(pattern, normalized_text)
    if match:
        amount = digits.convert_from_word((match.group(1)))
        currency_symbol = match.group(3)
    else:
        amount = digits.convert_from_word(normalized_text)
        if amount == 0:
            amount = 1
        pattern = r'([\w\d]+)\s+(تومان|ریال|ت)'
        match = re.search(pattern, normalized_text)
        if match:
            currency_symbol = match.group(2)

    if currency_symbol.strip() == 'تومان' or currency_symbol.strip() == 'ت':
        amount *= 10

    if 'هزاری' in normalized_text:
        amount *= 1000

    if not operator and mobile:
        operator = get_phone_operator(PhoneNumber(mobile=mobile))

    return amount, mobile, operator
