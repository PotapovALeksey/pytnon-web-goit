from .field import Field


class Address(Field):
    @staticmethod
    def validate(value):
        if not value:
            raise ValueError('The address is required')

    @Field.value.setter
    def value(self, value: str):
        self.validate(value)
        self._Field__value = value