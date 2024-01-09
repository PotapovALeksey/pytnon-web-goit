from user_assistant.class_fields.author import Author
from user_assistant.console.console import Console
from user_assistant.console.table_format.notes_table import note_titles, get_notes_row
from user_assistant.handlers.input_value import input_value

from .notes_abstract import NotesAbstract


class NotesSearchNotesByAuthorHandler(NotesAbstract):

    def execute(self):
        author = input_value('author', Author)
        result_notes = self.notes.search_by_author(author.value)
        Console.print_table(f"Notes found for tag: {author}", note_titles, list(map(get_notes_row,result_notes)))
