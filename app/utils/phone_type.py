

operator_enum = {
    'اعتباری': 1,
    'دائمی': 2,
    'دایمی': 2
}


def find_phone_type(sentence) -> int:
    for key, value in operator_enum.items():
        if key in sentence:
            return value
    return 1
