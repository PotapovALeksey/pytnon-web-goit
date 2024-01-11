from datetime import datetime
import re

from .field import Field


class Date(Field):
    DATE_FORMAT = "%d.%m.%Y"
    DATE_FORMAT_EXAMPLE = "12.10.1994"

    def __str__(self):
        return self.value.strftime(self.DATE_FORMAT)

    @classmethod
    def validate(cls, value: str):
        result = re.match(r"\d{2}\.\d{2}\.\d{4}", value)

        if result is None:
            raise ValueError(
                f"The date is incorrect. The format should be [{cls.DATE_FORMAT_EXAMPLE}]"
            )

    @Field.value.setter
    def value(self, value: str):
        self.validate(value)
        self._Field__value = datetime.strptime(value, self.DATE_FORMAT).date()
