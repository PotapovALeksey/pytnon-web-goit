from .field import Field


class Author(Field):
    @staticmethod
    def validate(value):
        if not value:
            raise ValueError('The author is required')

    @Field.value.setter
    def value(self, value: str):
        self.validate(value)
        self._Field__value = value