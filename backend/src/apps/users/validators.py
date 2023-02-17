import re

from tortoise.validators import Validator, ValidationError


class EmailValidator(Validator):
    domains = (
        'mail.ru',
        'yandex.ru',
        'gmail.com',
    )

    def __init__(self, flags: int = 0):
        self.regex = re.compile(
            r'^[A-z_\d]+@(?P<domain>[A-z]+\.[A-z]{2,3})$',
            flags
        )

    def __call__(self, value: str):
        if self.regex.match(value)['domain'] not in self.domains:
            raise ValidationError(f'This domain: `{self.domains}` is not accepted!')


class BasePhoneValidator(Validator):
    example: str
    pattern: str    # RawStr

    def __init__(self, flags: int = 0):
        self.regex = re.compile(
            self.pattern,
            flags
        )

    def __call__(self, value: str):
        if not self.regex.match(value):
            raise ValidationError(f'The phone number should look like this: {self.example}')


class RUPhoneValidator(BasePhoneValidator):
    example = '+79000000000'
    pattern = r'^(\+7|8)\d{10}$'
