from .field import Field
from datetime import datetime


class ID(Field):
    def __init__(self, init_id=None):
        super().__init__(
            init_id if init_id is not None else str(datetime.timestamp(datetime.now()))
        )
