from pathlib import Path

from .command_enum import CommandEnum

from .handlers.address_book.address_book_abstract import AddressBookAbstract
from .handlers.notes.notes_abstract import NotesAbstract

from .handlers.common.greeting import GreetingHandler
from .handlers.handler_factory import HandlerFactory

from .storages.csv_storage import CSVStorage
from .serializers.address_book.address_book_csv_serializer import (
    AddressBookCSVSerializer,
)
from .serializers.notes.notes_csv_serializer import NotesCSVSerializer

from .console.console import Console

STORAGE_PATH = Path(".") / Path("databases")

ADDRESS_BOOK_FIELDS = [
    "name",
    "birthday",
    "address",
    "phones",
    "mail",
    "updated_at",
    "created_at",
]
address_book_storage = CSVStorage(
    STORAGE_PATH, "address_book.csv", AddressBookCSVSerializer, ADDRESS_BOOK_FIELDS
)

NOTE_FIELDS = ["author", "text", "tags", "id", "updated_at", "created_at"]
notes_storage = CSVStorage(STORAGE_PATH, "notes.csv", NotesCSVSerializer, NOTE_FIELDS)


def main():
    AddressBookAbstract.initialize(address_book_storage)
    NotesAbstract.initialize(notes_storage)

    GreetingHandler().execute()

    while True:
        user_input = (
            Console.input("Enter command: ", CommandEnum.values()).casefold().strip()
        )

        handler = HandlerFactory.create_handler(user_input)

        if handler is None:
            Console.print_tip(
                "Enter [bold deep_sky_blue1]help[/] to see all possible CommandEnum"
            )
            continue

        if user_input in (CommandEnum.CLOSE.value, CommandEnum.EXIT.value):
            handler.execute()
            break

        handler.execute()
