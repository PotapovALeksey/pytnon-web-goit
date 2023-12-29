from user_assistant.class_fields.tag import Tag
from user_assistant.console.console import Console
from user_assistant.console.table_format.notes_table import note_titles, get_notes_row
from user_assistant.handlers.input_value import input_value

from .notes_abstract import NotesAbstract


class NotesSearchNotesByTagHandler(NotesAbstract):

    def execute(self):
        tag = input_value('tag', Tag)
        result_notes = self.notes.search_by_tags(tag.value)
        Console.print_table(f"Notes found for tag: {tag}", note_titles, list(map(get_notes_row,result_notes)))

