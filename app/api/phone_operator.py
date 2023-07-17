from ..schemas.phone_number_validation import PhoneNumber
from fastapi.encoders import jsonable_encoder


def get_phone_operator(data: PhoneNumber) -> str:
    phone_number = jsonable_encoder(data).get('mobile')
    operator_mapping = {
        '10': "همراه اول",
        '11': "همراه اول",
        '12': "همراه اول",
        '13': "همراه اول",
        '14': "همراه اول",
        '15': "همراه اول",
        '16': "همراه اول",
        '17': "همراه اول",
        '18': "همراه اول",
        '19': "همراه اول",
        '90': "همراه اول",
        '91': "همراه اول",
        '92': "همراه اول",
        '93': "همراه اول",
        '94': "همراه اول",
        '95': "همراه اول",
        '96': "همراه اول",
        '30': "ایرانسل",
        '33': "ایرانسل",
        '35': "ایرانسل",
        '36': "ایرانسل",
        '37': "ایرانسل",
        '38': "ایرانسل",
        '39': "ایرانسل",
        '01': "ایرانسل",
        '02': "ایرانسل",
        '03': "ایرانسل",
        '04': "ایرانسل",
        '05': "ایرانسل",
        '41': "ایرانسل",
        '00': "ایرانسل",
        '20': "رایتل",
        '21': "رایتل",
        '22': "رایتل",
        '23': "رایتل",
    }

    phone_digit = phone_number[-9:-7]
    return operator_mapping.get(phone_digit, "Unknown Operator")
