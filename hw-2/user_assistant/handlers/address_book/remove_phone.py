from user_assistant.class_fields.name import Name
from user_assistant.class_fields.phone import Phone
from user_assistant.console.console import Console
from user_assistant.console.table_format.address_book_table import address_book_titles, get_address_book_row
from user_assistant.handlers.input_value import input_value

from .address_book_abstract import AddressBookAbstract


class AddressBookRemovePhoneHandler(AddressBookAbstract):
    def execute(self):
        while True:
            name = input_value('contact name', Name)
            record = self.address_book.find(name.value)
            if record:
                break
            else:
                Console.print_error('Input existing name')

        phone = input_value('phone', Phone, placeholder=Phone.PHONE_FORMAT_EXAMPLE)

        if record.find_phone(phone):
            record.remove_phone(phone)
            self.storage.update(self.address_book.data.values())
            Console.print_table('Updated contact phone', address_book_titles, [get_address_book_row(record)])
        else:
            Console.print_error(f'Number {phone} is missing from the contact {name}')