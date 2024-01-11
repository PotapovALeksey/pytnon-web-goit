from datetime import datetime
from user_assistant.serializers.serializer import Serializer
from user_assistant.notes.note_record import NoteRecord
from user_assistant.class_fields.author import Author
from user_assistant.class_fields.tag import Tag
from user_assistant.class_fields.text import Text
from user_assistant.class_fields.id import ID
from user_assistant.class_fields.date_time import DateTime


class NotesCSVSerializer(Serializer):
    TAG_SEPARATOR = "|"

    @classmethod
    def serialize(cls, record: NoteRecord):
        return {
            "id": record.id.value,
            "created_at": str(record.created_at),
            "updated_at": str(record.updated_at),
            "author": record.author.value,
            "text": record.text.value,
            "tags": cls.TAG_SEPARATOR.join(record.str_tags),
        }

    @classmethod
    def deserialize(cls, record: NoteRecord):
        note_id = ID(record["id"])
        created_at = DateTime(
            datetime.strptime(record["created_at"], DateTime.DATE_TIME_FORMAT)
        )
        updated_at = DateTime(
            datetime.strptime(record["updated_at"], DateTime.DATE_TIME_FORMAT)
        )
        author = Author(record["author"])
        text = Text(record["text"])
        tags = list(map(lambda tag: Tag(tag), record["tags"].split(cls.TAG_SEPARATOR)))

        return NoteRecord(
            author=author,
            text=text,
            tags=tags,
            note_id=note_id,
            created_at=created_at,
            updated_at=updated_at,
        )
