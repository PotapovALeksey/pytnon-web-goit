from user_assistant.console.console import Console
from user_assistant.console.table_format.notes_table import note_titles, get_notes_row
from user_assistant.handlers.input_value import input_value

from .notes_abstract import NotesAbstract


class NotesRemoveTagsHandler(NotesAbstract):
    def execute(self):
        note_id = input_value('note ID', str)
        note = self.notes.find(note_id)

        if note is None:
            Console.print(f"No note found with ID {note_id}")
            return

        Console.print_table(f'Note updated with removed tags', note_titles, [get_notes_row(note)])
        while True:
            tags_input = input_value('selected tags to remove (separate by comma)', str, True).strip().casefold()

            if tags_input:
                tags_to_remove = set(filter(lambda tag: len(tag) > 0,  tags_input.split(',')))

                if not set(note.str_tags).issuperset(tags_to_remove):
                    Console.print_error(f'Tag missing in tags')
                    break
                else:
                    for tag in tags_to_remove:
                        if tag in note.tags:
                            note.remove_tag(tag)
                    self.storage.update(self.notes.data.values())
                    return Console.print_table(f'Note updated with removed tags', note_titles, [get_notes_row(note)])

            else:
                break


