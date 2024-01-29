from server.socket_server import socket_server, run_socket_server
from server.http_server import http_server
from threading import Thread
import logging
from pathlib import Path
from constant import STORAGE_FILE_PATH

logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")

storage = Path(STORAGE_FILE_PATH)

if not storage.exists():
    storage.parent.mkdir(exist_ok=True, parents=True)
    storage.touch()


if __name__ == "__main__":
    try:
        http_server_thread = Thread(target=http_server.serve_forever)
        socket_server_thread = Thread(target=run_socket_server, args=(socket_server,))

        http_server_thread.start()
        socket_server_thread.start()

    except KeyboardInterrupt:
        http_server.server_close()
        socket_server.close()
