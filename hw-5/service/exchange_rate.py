import aiohttp
import datetime
from typing import List, Tuple


class ExchangeRate:
    @staticmethod
    def get_exchange_date(days: int):
        today = datetime.date.today()
        exchange_data = today - datetime.timedelta(days=days)
        return exchange_data.strftime("%d.%m.%Y")

    @staticmethod
    def format_exchange_rate(rates: list):
        result = {}

        for rate in rates:
            result.update(
                {
                    rate.get("currency"): {
                        "sale": rate.get("saleRate", rate.get("saleRateNB")),
                        "purchase": rate.get(
                            "purchaseRate", rate.get("purchaseRateNB")
                        ),
                    }
                }
            )

        return result

    @classmethod
    def get_formatted_exchange_rate(cls, rates: List[dict], currencies: Tuple[str]):
        results = []

        for rate in rates:
            filtered_result = list(
                filter(
                    lambda item: item.get("currency") in currencies,
                    rate.get("exchangeRate"),
                )
            )

            formatted_result = cls.format_exchange_rate(filtered_result)

            results.append({rate.get("date"): formatted_result})

        return results

    async def get_archived_exchange_rates(self, days: int, currencies: Tuple[str]):
        exchange_dates = [self.get_exchange_date(day) for day in range(1, days + 1)]

        responses = []

        async with aiohttp.ClientSession() as session:
            for exchange_date in exchange_dates:
                try:
                    async with session.get(
                        f"https://api.privatbank.ua/p24api/exchange_rates?date={exchange_date}"
                    ) as response:
                        result = await response.json()

                        if response.status == 200:
                            responses.append(result)
                        else:
                            raise ValueError(result.get("message"))
                except aiohttp.ClientConnectorError as error:
                    raise error

        return self.get_formatted_exchange_rate(responses, currencies)
