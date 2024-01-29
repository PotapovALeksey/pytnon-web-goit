import socket
from config.socket_server_config import (
    SOCKET_HOST,
    SOCKET_PORT,
    SOCKET_DATA_SIZE,
)
import logging
import json
import urllib.parse
from datetime import datetime
from constant import STORAGE_FILE_PATH

socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def run_socket_server(socket_server):
    logging.info("Socket server has been started")
    socket_server.bind((SOCKET_HOST, SOCKET_PORT))

    while True:
        data, _ = socket_server.recvfrom(SOCKET_DATA_SIZE)

        logging.debug(f"Received data: {data}")

        if data:
            parsed_record = urllib.parse.unquote_plus(data.decode())

            record = {
                key: value
                for key, value in [el.split("=") for el in parsed_record.split("&")]
            }
            logging.debug(f"Record: {record}")

            try:
                with open(STORAGE_FILE_PATH, "r+", encoding="utf-8") as file:
                    try:
                        records = json.load(file)
                    except json.JSONDecodeError:
                        records = {}

                    logging.info(f"Records: {records}")

                    records.update({f"{datetime.today()}": record})

                    with open(STORAGE_FILE_PATH, "w", encoding="utf-8") as file:
                        json.dump(records, file, ensure_ascii=False, indent=4)
            except (ValueError, OSError) as error:
                logging.error(error)
