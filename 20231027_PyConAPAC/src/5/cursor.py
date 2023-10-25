class Cursor:
    def __init__(self, connection) -> None:
        self.conn = connection
        self.arraysize = 1

        self._context = None
        self._row_iter = None

        self._input_oids = ()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def execute(self, query, args=None):
        self.conn.execute(query, args)
        return self

    def fetchall(self):
        return self.conn.fetchall()

    def close(self):
        self.conn = None
