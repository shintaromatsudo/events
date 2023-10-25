import socket


class Server:
    def __init__(self, sock=None):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) if sock is None else sock

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __del__(self):
        self.close()

    def listen(self, host: str | None = None, port: int = 1111, timeout: int = 60):
        host = socket.gethostname() if host is None else host
        self.sock.settimeout(timeout)
        self.sock.bind((host, port))
        self.sock.listen(1)
        # print(f"Server {host}:{str(port)} started!")
        print(f"Server host:{str(port)} started!")

    def accept(self) -> socket.socket:
        client, address = self.sock.accept()
        # print(f"Connection from {address} has been established!")
        print(f"Connection from address has been established!")

        return client

    def receive(self, buffer: int = 1024) -> str:
        return self.sock.recv(buffer).decode("utf-8")

    def send(self, client: socket.socket, message: bytes) -> None:
        print("received>> ", message.decode("utf-8"))
        send_message = "Server accepted: " + message.decode("utf-8")
        client.send(send_message.encode("utf-8"))

    def close(self) -> None:
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
        except:
            pass

    def receive_client(self, client: socket.socket, buffer: int = 1024):
        with client:
            while True:
                try:
                    message_recv = client.recv(buffer)
                    if message_recv == b"":
                        break
                    self.send(client, message_recv)
                except ConnectionResetError:
                    break


if __name__ == "__main__":
    with Server() as server:
        server.listen()
        while True:
            try:
                client = server.accept()
                server.receive_client(client)
            except Exception as e:
                print(e)
                break
