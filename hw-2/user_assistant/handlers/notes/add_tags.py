from user_assistant.notes.notes import Notes
from user_assistant.storages.storage import Storage
from user_assistant.console.console import Console
from user_assistant.class_fields.tag import Tag
from user_assistant.handlers.input_value import input_value
from user_assistant.console.table_format.notes_table import note_titles, get_notes_row

from .notes_abstract import NotesAbstract


class NotesAddTagsHandlerHandler(NotesAbstract):
    def execute(self):
        note_id = input_value("Enter note ID", str)
        note = self.notes.find(note_id)

        if note is None:
            Console.print(f"No note found with ID {note_id}")
            return

        tags_input = input_value("Enter new tags (separate by comma)", str)
        new_tags = [Tag(tag.strip()) for tag in tags_input.split(",")]

        for tag in new_tags:
            note.add_tag(tag)

        self.storage.update(self.notes.data.values())

        # Використання Console.print_table для відображення оновленого запису
        Console.print_table(
            f"Note updated with new tags", note_titles, [get_notes_row(note)]
        )
