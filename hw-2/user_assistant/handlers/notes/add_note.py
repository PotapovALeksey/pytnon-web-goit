from user_assistant.class_fields.author import Author
from user_assistant.class_fields.tag import Tag
from user_assistant.class_fields.text import Text
from user_assistant.console.console import Console
from user_assistant.console.table_format.notes_table import note_titles, get_notes_row
from user_assistant.handlers.input_value import input_value
from user_assistant.notes.note_record import NoteRecord

from .notes_abstract import NotesAbstract


class NotesAddNoteHandler(NotesAbstract):
    def execute(self):
        author = input_value("author", Author)
        text = input_value("text", Text)
        tag = input_value("tag", Tag)

        note_record = NoteRecord(author=author, text=text, tags=[tag])
        self.notes.add_note(note_record)
        self.storage.update(self.notes.data.values())

        Console.print_table(f"Created note", note_titles, [get_notes_row(note_record)])
