import json
from models import Author, Quote
import sys
from queries import get_quotes_by_tags, get_quotes_by_tag, get_quotes_by_author_name
import connect

SEPARATOR = ":"
NAME_QUERY = "name"
TAG_QUERY = "tag"
TAGS_QUERY = "tags"
EXIT = "exit"


def cli_handler(input: str):
    if input.startswith(NAME_QUERY):
        author_name = input.replace(f"{NAME_QUERY}{SEPARATOR}", "").strip()

        print(get_quotes_by_author_name(author_name))

    if input.startswith(TAG_QUERY):
        tag = input.replace(f"{TAG_QUERY}{SEPARATOR}", "").strip()

        print(get_quotes_by_tag(tag))

    if input.startswith(TAGS_QUERY):
        tags = input.replace(f"{TAG_QUERY}{SEPARATOR}", "").strip().split(",")

        print(get_quotes_by_tags(tags))


def load_json_to_cloud():
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


if __name__ == "__main__":
    # load_json_to_cloud()

    while True:
        input_value = input("Enter query: ")

        if input_value == EXIT:
            sys.exit(0)

        cli_handler(input_value)
