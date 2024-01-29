import socket
from config.socket_server_config import (
    SOCKET_HOST,
    SOCKET_PORT,
)


def send_record(record):
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_client.sendto(record, (SOCKET_HOST, SOCKET_PORT))

    socket_client.close()
