from datetime import datetime

from user_assistant.class_fields.text import Text
from user_assistant.class_fields.author import Author
from user_assistant.class_fields.tag import Tag
from user_assistant.class_fields.date_time import DateTime
from user_assistant.class_fields.id import ID


class NoteRecord:
    def __init__(
        self,
        author: Author,
        text: Text,
        tags: [Tag],
        note_id=None,
        created_at=None,
        updated_at=None,
    ):
        self.author = author
        self.text = text
        self.tags = tags
        self.id = note_id if note_id is not None else ID()
        self.created_at = (
            created_at if created_at is not None else DateTime(datetime.now())
        )
        self.updated_at = (
            updated_at if updated_at is not None else DateTime(datetime.now())
        )

    def __str__(self):
        return f"Note author: {self.author.value}, text: {self.text.value}, tags: {'; '.join(p.value for p in self.tags)}, created_at: {self.created_at}, id: ${self.id.value}"

    def __repr__(self):
        return f"Note author: {self.author.value}, text: {self.text.value}, tags: {'; '.join(p.value for p in self.tags)}, created_at: {self.created_at}, id: ${self.id.value}"

    @property
    def str_tags(self):
        return list(map(lambda tag: tag.value, self.tags))

    @property
    def str_author(self):
        return self.author.value

    def update_updated_at(self):
        self.updated_at = DateTime(datetime.now())

    def update_text(self, new_text: Text):
        self.text = new_text
        self.update_updated_at()

    def update_author(self, new_author: Author):
        self.author = new_author
        self.update_updated_at()

    def add_tag(self, new_tag: Tag):
        self.tags.append(new_tag)
        self.update_updated_at()

    def remove_tag(self, tag: Tag):
        self.tags.remove(tag)
        self.update_updated_at()

    def edit_author(self, new_author: Author):
        self.author = new_author
        self.update_updated_at()

        return self.author

    def edit_text(self, new_text: Text):
        self.text = new_text
        self.update_updated_at()

        return self.text
