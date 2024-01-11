from user_assistant.console.console import Console
from user_assistant.console.table_format.notes_table import note_titles, get_notes_row

from .notes_abstract import NotesAbstract


class NotesSortByTagsHandler(NotesAbstract):
    def execute(self):
        result_sort = self.notes.sort_by_tags()

        Console.print_table(
            f"Sorted notes by tag: ", note_titles, list(map(get_notes_row, result_sort))
        )
