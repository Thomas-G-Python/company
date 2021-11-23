from django.core.exceptions import ValidationError
from datetime import date

"""
eigene Validator schreiben:
"""


def date_in_future_validator(date_):
    if date_ > date.today():
        # wenn das eintritt, ist das nicht legal!
        raise ValidationError("Das Datum darf nicht in der Zukunft liegen!")
    return date_


def name_validator(name_):
    if "@" in name_:
        raise ValidationError("bitte kein @ verwenden")
    return name_


def illegal_symbol_validator(name_):
    if "@" in name_:
        raise ValidationError("bitte kein @ verwenden")
    return name_


def digits_only_validator(value):
    if all(i.isdigit() for i in value):
        raise ValidationError ("Der Name darf nicht nur aus Zahlen bestehen!")
    return value


