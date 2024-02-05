from service.exchange_rate import ExchangeRate
from .websocket_handler import WebsocketHandler
from constant import MAX_AVAILABLE_DAYS


class ExchangeHandler(WebsocketHandler):
    name = "exchange"
    service = ExchangeRate()

    async def handle(self, request_str: str):
        rates_params = None

        try:
            params = request_str.split(" ")

            if len(params) > 1:
                name, *other_params = params
                days, *currencies = other_params

                parsed_days = (
                    MAX_AVAILABLE_DAYS if MAX_AVAILABLE_DAYS > int(days) else int(days)
                )

                rates_params = (parsed_days, currencies)
        except Exception:
            rates_params = (1, ("USD", "EUR"))
        finally:
            result = await self.service.get_archived_exchange_rates(*rates_params)

        return result
