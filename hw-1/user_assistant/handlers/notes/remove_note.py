from user_assistant.console.console import Console
from user_assistant.console.table_format.notes_table import note_titles, get_notes_row

from .notes_abstract import NotesAbstract


class NotesRemoveNoteHandler(NotesAbstract):
    def execute(self):
        value = Console.input("Input ID: ")

        result = self.notes.find(value)

        if result is not None:
            self.notes.delete(value)
            self.storage.update(self.notes.data.values())
            return Console.print_table(
                f"Remove note", note_titles, [get_notes_row(result)]
            )

        Console.print_error(f"There is no any notes named: {value}")
