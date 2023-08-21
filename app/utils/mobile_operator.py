import difflib


operator_enum = {
    'ایرانسل': 3,
    'همراه اول': 1,
    'رایتل': 2,
}


def find_operator_enum(word):
    for key, value in operator_enum.items():
        similarity_score = difflib.SequenceMatcher(None, key, word).ratio()
        if similarity_score >= 0.8:
            return value
