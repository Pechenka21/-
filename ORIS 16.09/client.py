import socket
import threading
import protocol

HOST = "127.0.0.1"
PORT = 9000


def receive_loop(sock):
    while True:
        try:
            result = protocol.recv_message(sock)

            if result is None:
                print("\n[сервер] соединение закрыто")
                break

            command, payload = result
            text = payload.decode("utf-8")

            if command == "TEXT":
                print(text)
            elif command == "ERRO":
                print(f"[ошибка] {text}")
            else:
                print(f"[{command}] {text}")

        except (ConnectionResetError, ConnectionError, OSError):
            print("\n[сервер] потеряно соединение")
            break


def send_loop(sock):
    while True:
        try:
            line = input()
        except EOFError:
            break

        line = line.strip()
        if not line:
            continue

        first, _, rest = line.partition(" ")
        first_upper = first.upper()

        if first_upper == "LIST":
            protocol.send_message(sock, "LIST", b"")

        elif first_upper == "QUIT":
            protocol.send_message(sock, "QUIT", b"")
            print("Отправлен QUIT, выходим...")
            break

        elif first_upper == "JOIN":
            protocol.send_message(sock, "JOIN", rest.encode("utf-8"))

        elif first_upper == "TEXT":
            protocol.send_message(sock, "TEXT", rest.encode("utf-8"))

        else:
            protocol.send_message(sock, "TEXT", line.encode("utf-8"))


def main():
    username = input("Введите имя: ").strip()
    if not username:
        print("Имя не может быть пустым")
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print(f"Подключено к {HOST}:{PORT}")

    try:
        protocol.send_message(sock, "JOIN", username.encode("utf-8"))

        listener = threading.Thread(target=receive_loop, args=(sock,), daemon=True)
        listener.start()

        send_loop(sock)

    finally:
        sock.close()
        print("Соединение закрыто")


if __name__ == "__main__":
    main()