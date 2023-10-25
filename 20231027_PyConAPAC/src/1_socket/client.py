import socket


class Client:
    def __init__(self, sock=None):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) if sock is None else sock

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def connect(self, host: str | None = None, port: int = 1111, timeout: int = 60) -> socket.socket:
        host = socket.gethostname() if host is None else host
        self.sock.settimeout(timeout)
        self.sock.connect((host, port))

        return self.sock

    def send(self, message: str = "") -> None:
        self.sock.send(message.encode("utf-8"))

    def receive(self, buffer: int = 1024) -> None:
        message = self.sock.recv(buffer).decode("utf-8")
        print(message)

    def close(self) -> None:
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
        except Exception as e:
            print(e)
            pass


if __name__ == "__main__":
    with Client() as client:
        client.connect()

        while True:
            message_send = input("> ")
            if message_send == "exit":
                break
            try:
                client.send(message_send)
                client.receive()
            except ConnectionResetError:
                break
