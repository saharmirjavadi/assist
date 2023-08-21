from ..schemas.phone_number_validation import PhoneNumber
from fastapi.encoders import jsonable_encoder


def get_phone_operator(data: PhoneNumber) -> str:
    phone_number = jsonable_encoder(data).get('mobile')
    operator_mapping = {
        '10': 1,
        '11': 1,
        '12': 1,
        '13': 1,
        '14': 1,
        '15': 1,
        '16': 1,
        '17': 1,
        '18': 1,
        '19': 1,
        '90': 1,
        '91': 1,
        '92': 1,
        '93': 1,
        '94': 1,
        '95': 1,
        '96': 1,
        '30': 3,
        '33': 3,
        '35': 3,
        '36': 3,
        '37': 3,
        '38': 3,
        '39': 3,
        '01': 3,
        '02': 3,
        '03': 3,
        '04': 3,
        '05': 3,
        '41': 3,
        '00': 3,
        '20': 2,
        '21': 2,
        '22': 2,
        '23': 2,
    }

    phone_digit = phone_number[-9:-7]
    return operator_mapping.get(phone_digit, "Unknown Operator")
