from user_assistant.console.console import Console
from user_assistant.console.table_format.notes_table import note_titles, get_notes_row

from .notes_abstract import NotesAbstract


class NotesFindNoteHandler(NotesAbstract):
    def execute(self):
        value = Console.input(f'Enter note id: ')

        result = self.notes.find(value)

        if result is not None:
            return Console.print_table(f'Found note', note_titles, [get_notes_row(result)])

        Console.print_error(f'There is no any contact named: {value}')