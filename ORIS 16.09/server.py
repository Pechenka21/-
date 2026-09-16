import socket
import threading
import protocol


HOST = "127.0.0.1"
PORT = 9000

clients = {}
lock = threading.Lock()


def broadcast(command, payload, exclude=None):
    with lock:
        targets = list(clients.keys())

    for sock in targets:
        if sock == exclude:
            continue
        try:
            protocol.send_message(sock, command, payload)
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass


def handle_client(conn, addr):
    username = None

    try:
        while True:
            result = protocol.recv_message(conn)   
            if result is None:
                break

            command, payload = result
            text = payload.decode("utf-8")

            if command == "JOIN":
                username = text
                with lock:
                    clients[conn] = username
                print(f"[JOIN] {addr} → {username}")
                # Уведомляем остальных
                broadcast("TEXT", f"[система] {username} присоединился".encode("utf-8"), exclude=conn)

            elif command == "TEXT":
                if username is None:
                    protocol.send_message(conn, "ERRO", "Сначала JOIN".encode("utf-8"))
                    continue
                print(f"[TEXT] {username}: {text}")
                broadcast("TEXT", f"[{username}]: {text}".encode("utf-8"), exclude=conn)

            elif command == "LIST":
                with lock:
                    names = list(clients.values())
                response = ", ".join(names) if names else "(никого)"
                protocol.send_message(conn, "TEXT", f"Пользователи: {response}".encode("utf-8"))

            elif command == "QUIT":
                print(f"[QUIT] {username}")
                break

            else:
                protocol.send_message(conn, "ERRO", f"Неизвестная команда: {command}".encode("utf-8"))

    except ConnectionResetError:
        print(f"[RESET] {addr} аварийно отключился")

    except ConnectionError:
        print(f"[CLOSE] {addr} соединение закрыто")

    finally:
        with lock:
            if conn in clients:
                name = clients.pop(conn)
            else:
                name = username
        try:
            conn.close()
        except OSError:
            pass
        if name:
            broadcast("TEXT", f"[система] {name} покинул чат".encode("utf-8"))


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Сервер запущен на {HOST}:{PORT}")

    try:
        while True:
            conn, addr = server.accept()
            print(f"[CONNECT] {addr}")
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()

    except KeyboardInterrupt:
        print("\nСервер остановлен (Ctrl+C)")

    finally:
        server.close()


if __name__ == "__main__":
    main()