from user_assistant.console.console import Console
from user_assistant.console.table_format.notes_table import note_titles, get_notes_row

from .notes_abstract import NotesAbstract


class NotesShowAllNotesHandler(NotesAbstract):
    def execute(self):
        Console.print_table('All notes', note_titles, list(map(get_notes_row, self.notes.data.values())))