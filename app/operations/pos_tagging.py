from hazm import word_tokenize, InformalNormalizer, POSTagger
from persian_tools import phone_number, digits
from ..utils.phone_operator import get_phone_operator
from ..utils.package_durations import find_package_duration
from persian import convert_fa_numbers
from ..schemas.phone_number_validation import PhoneNumber
from .pre_processing import sentence_normalizer
import difflib
import re
import os


def charge_pos_tagging(sentence):
    tagger = POSTagger(model=os.getcwd()+'/app/resources/pos_tagger.model')
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


def internet_pos_tagging(sentence):
    tagger = POSTagger(model=os.getcwd()+'/app/resources/pos_tagger.model')
    normalized_sentence = sentence_normalizer(sentence)

    tokenized_sentence = word_tokenize(normalized_sentence)
    tagged_sentence = tagger.tag(tokenized_sentence)

    mobile = None
    operator = None
    operators = ["ایرانسل", "همراه اول", "رایتل"]

    for word, tag in tagged_sentence:
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
        pattern = r"(\S+)\s+(گیگ|مگ|مگابایت|گیگابایت|گیگا)"
        match = re.search(pattern, normalized_sentence)
        if match:
            package_value = digits.convert_from_word((match.group(1)))
            package = f'{match.group(2)} {package_value}'

    package_duration = find_package_duration(normalized_sentence)
    if not operator and mobile:
        operator = get_phone_operator(PhoneNumber(mobile=mobile))

    return mobile, operator, package, package_duration
