from connection import Connection


class Client:
    def connect(self, user, host="localhost", port=5432, database=None, password=None, timeout=None):
        return Connection(user, host, port, database, password, timeout)
