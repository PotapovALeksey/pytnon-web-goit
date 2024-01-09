from collections import UserDict
from .address_book_record import AddressBookRecord
from pathlib import Path

CSV_STORAGE_PATH = Path('databases', 'address_book.csv')
FIELD_NAMES = ['name', 'birthday', 'phones']


class AddressBook(UserDict):
    def __init__(self, records: list[AddressBookRecord] = [], pagination_size: int = 50):
        self.pagination_size = pagination_size
        self.pagination_offset = 0

        self.data = {record.name.value.casefold(): record for record in records}

    def __iter__(self):
        return self

    def __next__(self):
        records = list(self.data.values())

        start_index = self.pagination_offset * self.pagination_size
        end_index = start_index + self.pagination_size

        if start_index < len(records):
            self.pagination_offset += 1
            return records[start_index:end_index]

        raise StopIteration

    def add(self, record: AddressBookRecord):
        self.data[record.name.value.casefold()] = record

        return self.data

    def find(self, name: str) -> AddressBookRecord | None:
        return self.data.get(name.casefold(), None)

    def delete(self, name: str):
        self.data.pop(name.casefold(), None)

        return self.data

    @staticmethod
    def is_existing_in_phone(value: str, record: AddressBookRecord):
        if len(record.phones) == 0:
            return False

        return list(filter(lambda phone: value in phone.value, record.phones))

    def search(self, value: str):
        return list(filter(
            lambda record: value.casefold() in record.name.value or self.is_existing_in_phone(value, record),
            self.data.values()
        ))
    
    def show_birthday(self, value: int):
        return list(filter(
            lambda record: AddressBookRecord.days_to_birthday(record) <= value,
            self.data.values()
        ))
