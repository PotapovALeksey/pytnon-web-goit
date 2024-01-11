from user_assistant.class_fields.name import Name
from user_assistant.console.console import Console
from user_assistant.console.table_format.address_book_table import (
    address_book_titles,
    get_address_book_row,
)
from user_assistant.handlers.input_value import input_value

from .address_book_abstract import AddressBookAbstract


class AddressBookRemoveContactHandler(AddressBookAbstract):
    def execute(self):
        name = input_value("name", Name)
        record = self.address_book.find(name.value)

        if record is not None:
            self.address_book.delete(name.value)
            self.storage.update(self.address_book.data.values())
            Console.print_success(f"Contact {name} removed")
            return

        Console.print_table(
            "Removed contact", address_book_titles, [get_address_book_row(record)]
        )
