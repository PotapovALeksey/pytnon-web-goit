from .field import Field


class Name(Field):
    @staticmethod
    def validate(value):
        if not value:
            raise ValueError("The name is required")

    @Field.value.setter
    def value(self, value: str):
        self.validate(value)
        self._Field__value = value
