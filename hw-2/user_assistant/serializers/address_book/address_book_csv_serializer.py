from datetime import datetime

from user_assistant.serializers.serializer import Serializer
from user_assistant.address_book.address_book_record import AddressBookRecord
from user_assistant.class_fields.name import Name
from user_assistant.class_fields.date import Date
from user_assistant.class_fields.phone import Phone
from user_assistant.class_fields.mail import Mail
from user_assistant.class_fields.address import Address
from user_assistant.class_fields.date_time import DateTime


class AddressBookCSVSerializer(Serializer):
    PHONE_SEPARATOR = "|"

    @classmethod
    def serialize(cls, record: AddressBookRecord):
        return {
            "phones": cls.PHONE_SEPARATOR.join(
                list(map(lambda phone: phone.value, record.phones))
            ),
            "name": record.name.value,
            "mail": record.mail.value,
            "address": record.address.value,
            "birthday": str(record.birthday),
            "created_at": str(record.created_at),
            "updated_at": str(record.updated_at),
        }

    @classmethod
    def deserialize(cls, record: AddressBookRecord):
        name = Name(record["name"])
        birthday = Date(record["birthday"])
        address = Address(record["address"])
        mail = Mail(record["mail"])
        phones = list(
            map(lambda phone: Phone(phone), record["phones"].split(cls.PHONE_SEPARATOR))
        )
        created_at = DateTime(
            datetime.strptime(record["created_at"], DateTime.DATE_TIME_FORMAT)
        )
        updated_at = DateTime(
            datetime.strptime(record["updated_at"], DateTime.DATE_TIME_FORMAT)
        )

        return AddressBookRecord(
            name, birthday, mail, address, phones, created_at, updated_at
        )
