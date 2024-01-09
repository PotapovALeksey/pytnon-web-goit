import re
from .field import Field


class Mail(Field):
    MAIL_FORMAT_EXAMPLE = 'john.petrov@gmail.com';

    @classmethod
    def validate(cls, value):
        result = re.match(r'^((([0-9A-Za-z]{1}[-0-9A-z\.]{0,30}[0-9A-Za-z]?)|([0-9А-Яа-я]{1}[-0-9А-я\.]{0,30}[0-9А-Яа-я]?))@([-A-Za-z]{1,}\.){1,}[-A-Za-z]{2,})$', value)

        if result is None:
            raise ValueError(f'The phone is incorrect. The format should be [{cls.MAIL_FORMAT_EXAMPLE}]')


    @Field.value.setter
    def value(self, value: str):
        self.validate(value)
        self._Field__value = value

      