from user_assistant.address_book.address_book_record import AddressBookRecord
from user_assistant.class_fields.address import Address
from user_assistant.class_fields.date import Date
from user_assistant.class_fields.mail import Mail
from user_assistant.class_fields.name import Name
from user_assistant.class_fields.phone import Phone
from user_assistant.console.console import Console
from user_assistant.console.table_format.address_book_table import address_book_titles, get_address_book_row
from user_assistant.handlers.input_value import input_value

from .address_book_abstract import AddressBookAbstract


class AddressBookAddContactHandler(AddressBookAbstract):
    def create_record(self):
        name = input_value('name', Name)

        if self.address_book.find(name.value) is not None:
            return Console.print_error(f'Contact {name.value} is already exist')

        date = input_value('date birthday', Date, placeholder=Date.DATE_FORMAT_EXAMPLE)
        mail = input_value('email', Mail, placeholder=Mail.MAIL_FORMAT_EXAMPLE)
        address = input_value('address', Address)
        phone = input_value('phone', Phone, placeholder=Phone.PHONE_FORMAT_EXAMPLE)

        return AddressBookRecord(name=name, birthday=date, mail=mail, address=address, phones=[phone])

    def execute(self):
        record = self.create_record()

        self.address_book.add(record)
        self.storage.update(self.address_book.data.values())

        Console.print_table('Created contact', address_book_titles, [get_address_book_row(record)])

