from user_assistant.console.console import Console
from user_assistant.command_enum import CommandEnum

from user_assistant.handlers.abstract_handler import AbstractHandler

column_titles = ['Command', 'Fields', 'Description']

address_book_documentation = [
    [CommandEnum.ADD_CONTACT.value, 'name, birthday, phone, address, mail', 'Create a new contact'],
    [CommandEnum.EDIT_CONTACT.value, 'name, birthday, address, mail', 'Edit an existing contact'],
    [CommandEnum.REMOVE_CONTACT.value, 'name', 'Remove an existing contact'],
    [CommandEnum.FIND_CONTACT.value, 'name', 'Find a contact by name'],
    [CommandEnum.ADD_PHONE.value, 'name, phone', 'Add a new phone for contact'],
    [CommandEnum.EDIT_PHONE.value, 'name', 'Edit an existing phone of contact'],
    [CommandEnum.REMOVE_PHONE.value, 'name', 'Remove an existing phone of contact'],
    [CommandEnum.SEARCH_CONTACTS.value, 'name or phone', 'Search contacts by name or phone'],
    [CommandEnum.SHOW_ALL_CONTACTS.value, '', 'Show all contacts'],
    [CommandEnum.SHOW_BIRTHDAY.value, 'days', 'Show contacts who birthdays will be in period of entered days'],
]

notes_documentation = [
    [CommandEnum.ADD_NOTE.value, 'author, text, tag', 'Create a new note'],
    [CommandEnum.EDIT_NOTE.value, 'id, author, text', 'Edit an existing note'],
    [CommandEnum.REMOVE_NOTE.value, 'id', 'Remove an existing contact'],
    [CommandEnum.FIND_NOTE.value, 'id', 'Find a note by id'],
    [CommandEnum.ADD_TAGS.value, 'id, tags', 'Add tags of note by id'],
    [CommandEnum.REMOVE_TAGS.value, 'id, tags', 'Remove tags of note by id'],
    [CommandEnum.SHOW_ALL_NOTES.value, '', 'Show all notes'],
    [CommandEnum.SEARCH_BY_TAG.value, 'tag', 'Search notes by tag'],
    [CommandEnum.SEARCH_BY_AUTHOR.value, 'author', 'Search notes by author'],
    [CommandEnum.SORT_BY_TAGS.value, '', 'Sort notes by tags'],
    [CommandEnum.SORT_BY_AUTHOR.value, '', 'Sort notes by author'],
]

sort_files_documentation = [
    [CommandEnum.SORT_FILES.value, 'folder', 'Sorting files inside folder by categories: music, image, video, documents'],
]

additional_CommandEnum_documentation = [
    [CommandEnum.EXIT.value, 'Exit from user assistant'],
    [CommandEnum.CLOSE.value, 'Exit from user assistant'],
    [CommandEnum.HELP.value, 'Show documentations'],
]


class HelpHandler(AbstractHandler):
    def execute(self):
        Console.print_table('Address book', column_titles, address_book_documentation)
        Console.print_table('Notes', column_titles, notes_documentation)
        Console.print_table('Sort files', column_titles, sort_files_documentation)
        Console.print_table('Additionals', list(filter(lambda title: title != 'Fields', column_titles)), additional_CommandEnum_documentation)