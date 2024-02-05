import asyncio

from websocket.websocket_server import run_ws_server

if __name__ == "__main__":
    try:
        asyncio.run(run_ws_server())
    except KeyboardInterrupt:
        print("\nShutdown")
