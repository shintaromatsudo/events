import socket
import threading


class Server:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __del__(self):
        self.close()

    def listen(self, port: int = 1111, timeout: int = 60):
        host = socket.gethostname()
        self.sock.settimeout(timeout)
        self.sock.bind((host, port))
        self.sock.listen(1)
        print(f"Server {host}:{str(port)} started!")

    def accept(self) -> [socket.socket, str]:
        client, address = self.sock.accept()
        print(f"Connection from {address} has been established!")

        return client, address

    def receive(self, buffer: int = 1024) -> str:
        return self.sock.recv(buffer).decode("utf-8")

    def respond(self, message: str) -> str:
        print("received>> ", message)
        return "Server accepted: " + message

    def close(self) -> None:
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
        except:
            pass

    def receive_client(self, client: socket.socket, address: str, buffer: int = 1024):
        with client:
            while True:
                try:
                    message_recv = client.recv(buffer)
                    if message_recv == b"":
                        break
                    message_resp = self.respond(message_recv.decode("utf-8"))
                    client.send(message_resp.encode("utf-8"))
                except ConnectionResetError:
                    break


if __name__ == "__main__":
    with Server() as server:
        server.listen()
        while True:
            try:
                client, address = server.accept()

                thread = threading.Thread(target=server.receive_client, args=(client, address))
                thread.start()
            except Exception as e:
                print(e)
                break
