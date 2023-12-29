from typing import Type
from user_assistant.storages.storage import Storage
from user_assistant.address_book.address_book import AddressBook
from user_assistant.handlers.abstract_handler import AbstractHandler


class AddressBookAbstract(AbstractHandler):
    storage = None
    address_book = None

    @classmethod
    def initialize(cls, storage: Type[Storage]):
        cls.storage = storage
        cls.address_book = AddressBook(cls.storage.get())
