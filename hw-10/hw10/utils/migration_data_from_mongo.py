import os
import django

from pymongo import MongoClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw10.settings")
django.setup()

from quotes.models import Author, Tag, Quote  # noqa

client = MongoClient(
    "mongodb+srv://alexfullstack:alexfullstack@cluster.uqblvyc.mongodb.net/"
)

db = client.python

authors = db.authors.find()

for author in authors:
    Author.objects.get_or_create(
        fullname=author["fullname"],
        born_date=author["born_date"],
        born_location=author["born_location"],
        description=author["description"],
    )


quotes = db.quotes.find()

for quote in quotes:
    tags = []
    for tag in quote["tags"]:
        t, *_ = Tag.objects.get_or_create(tag=tag)
        tags.append(t)

    is_exist_quote = Quote.objects.filter(quote=quote["quote"])

    if not is_exist_quote:
        author = db.authors.find_one({"_id": quote["author"]})
        a = Author.objects.get(fullname=author["fullname"])
        q = Quote.objects.create(
            quote=quote["quote"],
            author=a,
        )

        for tag in tags:
            q.tags.add(tag)
