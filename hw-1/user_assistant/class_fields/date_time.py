from datetime import datetime

from .field import Field


class DateTime(Field):
    DATE_TIME_FORMAT = '%d.%m.%Y %H:%M:%S'

    def __str__(self):
        return self.value.strftime(self.DATE_TIME_FORMAT)

    @staticmethod
    def validate(value: datetime):
        if not isinstance(value, datetime):
            raise ValueError('The datetime is incorrect')

    @Field.value.setter
    def value(self, value: datetime):
        self.validate(value)
        self._Field__value = value
