from user_assistant.class_fields.name import Name
from user_assistant.console.console import Console
from user_assistant.console.table_format.address_book_table import address_book_titles, get_address_book_row
from user_assistant.handlers.input_value import input_value

from .address_book_abstract import AddressBookAbstract


class AddressBookFindContactHandler(AddressBookAbstract):

    def execute(self):
        name = input_value('name', Name)

        record = self.address_book.find(name.value)

        if record is not None:
            return Console.print_table('Found contact', address_book_titles, [get_address_book_row(record)])

        Console.print_error(f'There is no any contact named: {name}')