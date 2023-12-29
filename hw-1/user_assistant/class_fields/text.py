from .field import Field


class Text(Field):
    @staticmethod
    def validate(value):
        if not value:
            raise ValueError('The text is required')

    @Field.value.setter
    def value(self, value: str):
        self.validate(value)
        self._Field__value = value