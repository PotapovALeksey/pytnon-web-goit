from user_assistant.console.console import Console
from user_assistant.console.table_format.address_book_table import address_book_titles, get_address_book_row

from .address_book_abstract import AddressBookAbstract


class AddressBookShowAllContactsHandler(AddressBookAbstract):
    def execute(self):
        Console.print_table('All contacts', address_book_titles, list(map(get_address_book_row, self.address_book.data.values())))