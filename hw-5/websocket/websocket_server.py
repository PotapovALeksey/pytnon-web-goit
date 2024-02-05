import logging
import websockets
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
from websocket.websocket_handler.websocket_exchange_handler import ExchangeHandler
from websocket.websocket_handler.websocket_handler import WebsocketHandler
from typing import List

logging.basicConfig(level=logging.INFO)


class Server:
    clients = set()

    def __init__(self, handlers: List[WebsocketHandler] = []):
        self.handlers = {handler.name: handler for handler in handlers}

        print(self.handlers)

    async def register(self, ws: WebSocketServerProtocol):
        self.clients.add(ws)
        logging.info(f"{ws.remote_address} connects")

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f"{ws.remote_address} disconnects")

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distribute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            for handler_name in self.handlers:
                if message.startswith(handler_name):
                    await ws.send("Exchange request is in progress...")
                    result = await self.handlers[handler_name].handle(message)
                    await ws.send(f"Exchange rates: {result}")
                    continue

            for client in self.clients:
                if client != ws:
                    await client.send(f"{ws.remote_address}: {message}")


async def run_ws_server():
    server = Server([ExchangeHandler()])

    async with websockets.serve(server.ws_handler, "localhost", 8765) as server:
        await server.server.serve_forever()
