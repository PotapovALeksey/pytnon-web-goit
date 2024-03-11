import sys
import asyncio

from database_service.queries import (
    get_quotes_by_tags,
    get_quotes_by_tag,
    get_quotes_by_author_name,
)
from scraping_service.scraping import run_scraping
from load_data_to_cloud import load_data_to_cloud

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


if __name__ == "__main__":
    asyncio.run(run_scraping())

    load_data_to_cloud()

    while True:
        input_value = input("Enter query: ")

        if input_value == EXIT:
            sys.exit(0)

        cli_handler(input_value)
