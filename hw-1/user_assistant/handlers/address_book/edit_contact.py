from user_assistant.class_fields.address import Address
from user_assistant.class_fields.date import Date
from user_assistant.class_fields.mail import Mail
from user_assistant.class_fields.name import Name
from user_assistant.console.console import Console
from user_assistant.console.table_format.address_book_table import (
    address_book_titles,
    get_address_book_row,
)
from user_assistant.handlers.input_value import input_value
from .address_book_abstract import AddressBookAbstract

FIELDS_CLASS = {
    "name": (Name, None),
    "birthday": (Date, Date.DATE_FORMAT_EXAMPLE),
    "email": (Mail, Mail.MAIL_FORMAT_EXAMPLE),
    "address": (Address, None),
}


class AddressBookEditContactHandler(AddressBookAbstract):
    def edit_contact(self):
        Console.print_tip("Press “Enter” with empty value to skip")

        name = Console.input("Enter contact name: ")

        if not name:
            return

        record = self.address_book.find(name)

        if record is None:
            return Console.print_error("Input existing name")

        for field in FIELDS_CLASS.keys():
            field_class, placeholder = FIELDS_CLASS[field]
            volume = input_value(
                f"new {field}", field_class, True, placeholder=placeholder
            )

            if field == "birthday" and volume:
                record.edit_birthday(volume)
            elif field == "email" and volume:
                record.edit_email(volume)
            elif field == "address" and volume:
                record.edit_address(volume)
            elif field == "name" and volume:
                self.address_book.delete(str(record.name))
                record.edit_name(volume)
                self.address_book.add(record)

        self.storage.update(self.address_book.data.values())

        Console.print_table(
            "Updated contact", address_book_titles, [get_address_book_row(record)]
        )

    def execute(self):
        self.edit_contact()
