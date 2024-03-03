from mongoengine import Document
from mongoengine.fields import StringField, ListField, ReferenceField


class Author(Document):
    fullname = StringField(max_length=50, required=True)
    born_date = StringField(required=True)
    born_location = StringField(max_length=100, required=True)
    description = StringField(required=True)
    meta = {"collection": "authors"}


class Quote(Document):
    tags = ListField(StringField(max_length=40))
    author = ReferenceField(Author)
    quote = StringField(required=True)
    meta = {"collection": "quotes"}
