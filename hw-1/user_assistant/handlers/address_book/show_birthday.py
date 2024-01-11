from user_assistant.console.console import Console
from user_assistant.console.table_format.address_book_table import (
    address_book_titles,
    get_address_book_row,
)
from .address_book_abstract import AddressBookAbstract


class AddressBookShowBirthdayHandler(AddressBookAbstract):
    def execute(self):
        while True:
            try:
                days = int(Console.input(f"Enter number of days: "))
                if days in range(1, 365):
                    break
                else:
                    Console.print_error("Days must be in interval 1-365")
                    continue
            except:
                Console.print_error("Days may be an integer")

        records = self.address_book.show_birthday(days)

        Console.print_table(
            f"All contacts that birthday will be earlier then {days} days",
            address_book_titles,
            list(map(get_address_book_row, records)),
        )
