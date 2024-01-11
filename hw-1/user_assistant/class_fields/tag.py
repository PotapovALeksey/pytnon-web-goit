from .field import Field


class Tag(Field):
    def __eq__(self, other: str):
        return self.value == other

    @Field.value.setter
    def value(self, value: str):
        self._Field__value = value.casefold()
