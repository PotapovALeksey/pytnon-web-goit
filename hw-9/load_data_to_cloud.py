import json
from database_service.models import Author, Quote


def load_data_to_cloud():
    with open("data/authors.json", "r") as f:
        authors = json.load(f)

    with open("data/quotes.json", "r") as f:
        quotes = json.load(f)

    for author in authors:
        Author(
            fullname=author["fullname"],
            born_date=author["born_date"],
            born_location=author["born_location"],
            description=author["description"],
        ).save()

    for quote in quotes:
        author = Author.objects.get(fullname=quote["author"])

        if author:
            Quote(
                author=author,
                tags=quote["tags"],
                quote=quote["quote"],
            ).save()
