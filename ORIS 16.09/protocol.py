import struct
import socket


MAX_MESSAGE_SIZE = 10 * 1024 * 1024   # 10 МБ
HEADER_SIZE = 8

def recv_exact(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if chunk == b"":
            raise ConnectionError("Соединение закрыто до получения всех данных")
        data += chunk
    return data


def send_message(sock, command, payload):
    cmd_bytes = command.encode("utf-8")
    header = struct.pack("!4sI", cmd_bytes, len(payload))
    sock.sendall(header + payload)


def recv_message(sock):
    try:
        header = recv_exact(sock, HEADER_SIZE)
    except ConnectionError:
        return None

    command_bytes, length = struct.unpack("!4sI", header)
    command = command_bytes.decode("utf-8")

    if length > MAX_MESSAGE_SIZE:
        raise ValueError("Слишком большое сообщение")

    if length > 0:
        payload = recv_exact(sock, length)
    else:
        payload = b""

    return command, payload                                 