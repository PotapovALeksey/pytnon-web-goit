import asyncio
import aiohttp
import json
from bs4 import BeautifulSoup

url = "https://quotes.toscrape.com"


def get_author_urls(soup: BeautifulSoup):
    author_urls = set()

    authors = soup.select(".quote span a")

    for author in authors:
        author_urls.add(author["href"])

    return author_urls


def get_quotes(soup: BeautifulSoup):
    quotes = []

    local_quotes = soup.findAll("div", {"class": "quote"})

    for quote in local_quotes:
        author_name = quote.find("small", {"class": "author"}).text.strip()

        if author_name.startswith('Alexandre Dumas'):
            author_name = 'Alexandre Dumas-fils'

        quotes.append(
            {
                "quote": quote.find("span", {"class": "text"}).text.strip(),
                "author": author_name,
                "tags": [
                    tag.text.strip() for tag in quote.findAll("a", {"class": "tag"})
                ],
            }
        )

    return quotes


def get_author(soup: BeautifulSoup):
    return {
        "fullname": soup.find("h3", {"class": "author-title"}).text.strip(),
        "born_date": soup.find("span", {"class": "author-born-date"}).text.strip(),
        "born_location": soup.find(
            "span", {"class": "author-born-location"}
        ).text.strip(),
        "description": soup.find("div", {"class": "author-description"}).text.strip(),
    }


async def scrape_quotes_and_author_urls(session: asyncio, page_url=""):
    quotes = []
    author_urls = set()

    local_url = f"{url}{page_url}"

    async with session.get(local_url) as response:
        try:
            if response.status == 200:
                result = await response.text()

                soup = BeautifulSoup(result, "html.parser")

                author_urls.update(get_author_urls(soup))
                quotes.extend(get_quotes(soup))

                next_button_wrapper = soup.find("li", {"class": "next"})
                next_page_url = (
                    next_button_wrapper.find("a")["href"]
                    if next_button_wrapper is not None
                    else None
                )

                if next_page_url is not None:
                    next_quotes, next_author_urls = await scrape_quotes_and_author_urls(
                        session, next_page_url
                    )

                    author_urls.update(next_author_urls)
                    quotes.extend(next_quotes)

        except aiohttp.ClientConnectorError as err:
            print(f"Connection error: {url}", str(err))

        return quotes, author_urls


async def scrape_authors(session, author_urls: list[str]):
    authors = []

    for author_url in author_urls:
        async with session.get(f"{url}{author_url}") as response:
            try:
                if response.status == 200:
                    result = await response.text()

                    soup = BeautifulSoup(result, "html.parser")

                    authors.append(get_author(soup))

            except aiohttp.ClientConnectorError as err:
                print(f"Connection error: {url}", str(err))

    return authors


def write_data_to_file(quotes, authors):
    with open("data/quotes.json", "w") as f:
        json.dump(quotes, f, indent=2, ensure_ascii=False)

    with open("data/authors.json", "w") as f:
        json.dump(authors, f, indent=2, ensure_ascii=False)


async def run_scraping():
    async with aiohttp.ClientSession() as session:
        quotes, author_urls = await scrape_quotes_and_author_urls(session)
        print("quotes", quotes)
        print("author_urls", author_urls)
        authors = await scrape_authors(session, list(author_urls))

        print("authors", authors)

    write_data_to_file(quotes, authors)
