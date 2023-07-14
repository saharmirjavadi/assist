from sklearn.feature_extraction.text import CountVectorizer
from hazm import word_tokenize, POSTagger
from hazm import word_tokenize, InformalNormalizer
from persian_tools import phone_number, digits
from persian import convert_fa_numbers
from joblib import load
import difflib
import re
import os


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
    normalizer = InformalNormalizer()
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
    loaded_model = load(os.getcwd()+'/app/models/nb-model.joblib')
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
    normalized_sentence = InformalNormalizer(
        correct_spacing=True, remove_specials_chars=True).normalize(sentence)
    normalized_sentence = [''.join(ele) for ele in normalized_sentence[0]]
    normalized_sentence = " ".join(normalized_sentence)

    tokenized_sentence = word_tokenize(normalized_sentence)
    tagged_sentence = tagger.tag(tokenized_sentence)
    # print(tagged_sentence)
    # print(tagger.data_maker(tokens=[tokenized_sentence]))

    amount = None
    number = None
    operator = None
    operators = ["ایرانسل", "همراه اول", "رایتل"]

    for word, tag in tagged_sentence:
        # print(tag, word)
        if tag == 'NUM':
            num = convert_fa_numbers(word)
            if phone_number.validate(num):
                number = num

        for keyword in operators:
            similarity_score = difflib.SequenceMatcher(
                None, keyword, word).ratio()
            if similarity_score >= 0.8:
                operator = keyword

    pattern = r'(\w+)\s+(?:تومان|تومن|ریال|ت)'

    # Find the amount
    match = re.search(pattern, sentence)
    amount = digits.convert_from_word((match.group(1)))

    return amount, number, operator
