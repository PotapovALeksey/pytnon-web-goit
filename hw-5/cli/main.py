import asyncio
import argparse
from service.exchange_rate import ExchangeRate
import logging

parser = argparse.ArgumentParser(
    description="App for getting currency exchange information"
)
parser.add_argument("-d", "--days", type=int)
parser.add_argument("-c", "--currencies", nargs="+", default=["EUR", "USD"])
args = vars(parser.parse_args())
days = args.get("days")
currencies = args.get("currencies")

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


async def main():
    exchange_service = ExchangeRate()

    try:
        result = await exchange_service.get_archived_exchange_rates(days, currencies)
        logging.info(f"{result}")
    except Exception as error:
        logging.error(f"{error}")


if __name__ == "__main__":
    if days <= 10:
        asyncio.run(main())
    else:
        logging.error("Number of days must be less than 10")
