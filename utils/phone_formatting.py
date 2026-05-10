from phonenumbers import (PhoneNumberFormat, format_number, is_valid_number,
                          parse)
from phonenumbers.phonenumberutil import NumberParseException


def format_phone_number(phone: str) -> str | None:
    try:
        phone_number = parse(phone, "UA")
        if not is_valid_number(phone_number):
            return None
        return format_number(phone_number, PhoneNumberFormat.INTERNATIONAL)
    except NumberParseException:
        return None
