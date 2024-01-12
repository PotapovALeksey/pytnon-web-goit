from collections import UserDict
from .note_record import NoteRecord


class Notes(UserDict):
    def __init__(self, records: list[NoteRecord] = []):
        self.data = {record.id.value: record for record in records}

    def add_note(self, note: NoteRecord):
        self.data[note.id.value] = note

    def sort_by_tags(self):
        sorted_notes = sorted(
            self.data.values(), key=lambda note: ",".join(note.str_tags)
        )
        return sorted_notes

    def sort_by_author(self):
        sorted_notes = sorted(
            self.data.values(), key=lambda note: ",".join(note.str_author.casefold())
        )
        return sorted_notes

    def delete(self, id: str):
        return self.data.pop(id, None)

    def find(self, id: str):
        return self.data.get(id, None)

    def search_by_tags(self, tag_name):
        return list(
            filter(
                lambda note: tag_name.casefold() in note.str_tags, self.data.values()
            )
        )

    def search_by_author(self, author: str):
        return list(
            filter(
                lambda note: note.str_author.casefold() == author.casefold(),
                self.data.values(),
            )
        )
