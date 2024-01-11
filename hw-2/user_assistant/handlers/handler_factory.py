from user_assistant.command_enum import CommandEnum

from .address_book.add_contact import AddressBookAddContactHandler
from .address_book.remove_contact import AddressBookRemoveContactHandler
from .address_book.edit_contact import AddressBookEditContactHandler
from .address_book.find_contact import AddressBookFindContactHandler
from .address_book.show_birthday import AddressBookShowBirthdayHandler
from .address_book.show_all_contacts import AddressBookShowAllContactsHandler
from .address_book.search_contact import AddressBookSearchContactsHandler
from .address_book.add_phone import AddressBookAddPhoneHandler
from .address_book.edit_phone import AddressBookEditPhoneHandler
from .address_book.remove_phone import AddressBookRemovePhoneHandler

from .notes.add_note import NotesAddNoteHandler
from .notes.find_note import NotesFindNoteHandler
from .notes.remove_note import NotesRemoveNoteHandler
from .notes.search_notes_by_author import NotesSearchNotesByAuthorHandler
from .notes.search_notes_by_tag import NotesSearchNotesByTagHandler
from .notes.edit_note import NotesEditNoteHandler
from .notes.sort_by_tags import NotesSortByTagsHandler
from .notes.sort_by_author import NotesSortByAuthorHandler
from .notes.remove_tags import NotesRemoveTagsHandler
from .notes.add_tags import NotesAddTagsHandlerHandler
from .notes.show_all_notes import NotesShowAllNotesHandler

from .common.help import HelpHandler
from .common.exit import ExitHandler
from .sort_file.sort_file import SortFileHandler

handlers = {
    CommandEnum.ADD_CONTACT.value: AddressBookAddContactHandler,
    CommandEnum.REMOVE_CONTACT.value: AddressBookRemoveContactHandler,
    CommandEnum.EDIT_CONTACT.value: AddressBookEditContactHandler,
    CommandEnum.FIND_CONTACT.value: AddressBookFindContactHandler,
    CommandEnum.SHOW_BIRTHDAY.value: AddressBookShowBirthdayHandler,
    CommandEnum.SHOW_ALL_CONTACTS.value: AddressBookShowAllContactsHandler,
    CommandEnum.SEARCH_CONTACTS.value: AddressBookSearchContactsHandler,
    CommandEnum.ADD_PHONE.value: AddressBookAddPhoneHandler,
    CommandEnum.EDIT_PHONE.value: AddressBookEditPhoneHandler,
    CommandEnum.REMOVE_PHONE.value: AddressBookRemovePhoneHandler,
    CommandEnum.ADD_NOTE.value: NotesAddNoteHandler,
    CommandEnum.FIND_NOTE.value: NotesFindNoteHandler,
    CommandEnum.EDIT_NOTE.value: NotesEditNoteHandler,
    CommandEnum.REMOVE_NOTE.value: NotesRemoveNoteHandler,
    CommandEnum.SHOW_ALL_NOTES.value: NotesShowAllNotesHandler,
    CommandEnum.SEARCH_BY_TAG.value: NotesSearchNotesByTagHandler,
    CommandEnum.SEARCH_BY_AUTHOR.value: NotesSearchNotesByAuthorHandler,
    CommandEnum.SORT_BY_TAGS.value: NotesSortByTagsHandler,
    CommandEnum.SORT_BY_AUTHOR.value: NotesSortByAuthorHandler,
    CommandEnum.REMOVE_TAGS.value: NotesRemoveTagsHandler,
    CommandEnum.ADD_TAGS.value: NotesAddTagsHandlerHandler,
    CommandEnum.SORT_FILES.value: SortFileHandler,
    CommandEnum.EXIT.value: ExitHandler,
    CommandEnum.CLOSE.value: ExitHandler,
    CommandEnum.HELP.value: HelpHandler,
}


class HandlerFactory:
    @staticmethod
    def create_handler(command: str):
        if command in handlers:
            return handlers[command]()

        return None
