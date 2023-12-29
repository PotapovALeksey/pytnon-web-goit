from typing import Type
from user_assistant.storages.storage import Storage
from user_assistant.notes.notes import Notes
from user_assistant.handlers.abstract_handler import AbstractHandler


class NotesAbstract(AbstractHandler):
    storage = None
    notes = None

    @classmethod
    def initialize(cls, storage: Type[Storage]):
        cls.storage = storage
        cls.notes = Notes(cls.storage.get())
