from database_service.models import Author, Quote
from database_service.redis_cache import cache
import database_service.connect


@cache
def get_quotes_by_author_name(author_name: str):
    author = Author.objects(fullname__iregex=author_name).first()

    if author:
        quotes = Quote.objects(author=author)

        return [quote.to_mongo().to_dict() for quote in quotes]


@cache
def get_quotes_by_tag(tag: str):
    quotes = Quote.objects(tags__iregex=tag)

    return [quote.to_mongo().to_dict() for quote in quotes]


@cache
def get_quotes_by_tags(tags: list[str]):
    quotes = Quote.objects(tags__in=tags)

    return [quote.to_mongo().to_dict() for quote in quotes]
