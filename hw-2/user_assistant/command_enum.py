from .utils import ExtendedEnum


class CommandEnum(ExtendedEnum):
    ADD_CONTACT = "add_contact"
    REMOVE_CONTACT = "remove_contact"
    EDIT_CONTACT = "edit_contact"
    FIND_CONTACT = "find_contact"
    SHOW_BIRTHDAY = "show_birthday"
    SHOW_ALL_CONTACTS = "show_all_contacts"
    SEARCH_CONTACTS = "search_contacts"
    ADD_PHONE = "add_phone"
    EDIT_PHONE = "edit_phone"
    REMOVE_PHONE = "remove_phone"

    ADD_NOTE = "add_note"
    FIND_NOTE = "find_note"
    SHOW_ALL_NOTES = "show_all_notes"
    REMOVE_NOTE = "remove_note"

    SEARCH_BY_TAG = "search_by_tag"
    SEARCH_BY_AUTHOR = "search_by_author"
    EDIT_NOTE = "edit_note"
    SORT_BY_TAGS = "sort_by_tags"
    SORT_BY_AUTHOR = "sort_by_author"
    REMOVE_TAGS = "remove_tags"
    ADD_TAGS = "add_tags"

    SORT_FILES = "sort_files"

    HELP = "help"

    EXIT = "exit"
    CLOSE = "close"
