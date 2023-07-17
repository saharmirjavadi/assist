from pydantic import BaseModel, validator


class PhoneNumber(BaseModel):
    mobile: str

    @validator('mobile')
    def validate_mobile_number(cls, mobile):
        if not mobile or not mobile.isdigit() or len(mobile) not in [10, 11]:
            return 'unkown'
        return mobile
