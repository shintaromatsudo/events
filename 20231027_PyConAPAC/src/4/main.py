import socket
from struct import Struct

import scramp


# Connect
class Client:
    def __init__(self):
        self.NULL_BYTE = b"\x00"
        self._encode = "utf8"
        self.user = "postgres".encode(self._encode)
        self.database = "postgres".encode(self._encode)
        self.password = "postgres".encode(self._encode)

        self.rows = []
        self.columns = []

    def socket(self):
        host = "localhost"
        port = 5432
        timeout = 60

        sock = socket.create_connection((host, port), timeout)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        # makefile() is a convenience function to create a stream socket
        self._sock = sock.makefile("rwb")

    def connect(self):
        protocol = 196608
        init_val = bytearray(Struct(f"!i").pack(protocol))
        init_val.extend("user".encode("ascii") + self.NULL_BYTE + self.user + self.NULL_BYTE)
        init_val.extend("database".encode("ascii") + self.NULL_BYTE + self.database + self.NULL_BYTE)
        init_val.extend(self.NULL_BYTE)

        self._sock.write(Struct(f"!i").pack(len(init_val) + 4))
        self._sock.write(init_val)
        self._sock.flush()

    def authenticate(self):
        AUTHENTICATION_REQUEST = b"R"
        PARAMETER_STATUS = b"S"
        BACKEND_KEY_DATA = b"K"
        READY_FOR_QUERY = b"Z"

        code = None

        while code != READY_FOR_QUERY:
            code, data_len_with_myself = self._receive_head()
            data_len = data_len_with_myself - 4
            data = self._read(data_len)
            if code == AUTHENTICATION_REQUEST:
                self.handle_authentication_request(data)
            elif code == PARAMETER_STATUS:
                self.handle_parameter_status(data)
            elif code == BACKEND_KEY_DATA:
                self.handle_backend_key_data(data)
            elif code == READY_FOR_QUERY:
                self.handle_ready_for_query(data)

    def _receive_head(self):
        code, data_len_with_myself = Struct(f"!ci").unpack_from(self._read(5))
        return code, data_len_with_myself

    def _send_messages(self, code, data):
        self._write(code)
        self._write(Struct(f"!i").pack(len(data) + 4))
        self._write(data)

    def _read(self, size):
        got = 0
        buff = []
        while got < size:
            block = self._sock.read(size - got)
            if block == b"":
                raise Exception("unexpected EOF")
            got += len(block)
            buff.append(block)

        return b"".join(buff)

    def _write(self, d):
        try:
            self._sock.write(d)
        except OSError as e:
            raise Exception("network error") from e

    def _write_flush(self):
        FLUSH = b"H"
        FLUSH_MSG = FLUSH + Struct(f"!i").pack(4)
        self._write(FLUSH_MSG)

    def _write_sync(self):
        SYNC = b"S"
        SYNC_MSG = SYNC + Struct(f"!i").pack(4)
        self._write(SYNC_MSG)

    def handle_authentication_request(self, data) -> None:
        print("handle_authentication_request")
        auth_code = Struct(f"!i").unpack_from(data)[0]

        PASSWORD = b"p"

        if auth_code == 0:
            pass

        elif auth_code == 10:
            # AuthenticationSASL
            mechanisms = [m.decode("ascii") for m in data[4:-2].split(self.NULL_BYTE)]

            self.auth = scramp.ScramClient(
                mechanisms,
                self.user.decode(self._encode),
                self.password.decode(self._encode),
                channel_binding=None,
            )

            init = self.auth.get_client_first().encode(self._encode)
            mechanism = self.auth.mechanism_name.encode("ascii") + self.NULL_BYTE

            # SASLInitialResponse
            self._write(PASSWORD)
            self._write(Struct(f"!i").pack(len(mechanism + Struct(f"!i").pack(len(init)) + init) + 4))
            self._write(mechanism + Struct(f"!i").pack(len(init)) + init)
            self._sock.flush()

        elif auth_code == 11:
            # AuthenticationSASLContinue
            self.auth.set_server_first(data[4:].decode(self._encode))

            # SASLResponse
            msg = self.auth.get_client_final().encode(self._encode)
            self._write(PASSWORD)
            self._write(Struct(f"!i").pack(len(msg) + 4))
            self._write(msg)
            self._sock.flush()

        elif auth_code == 12:
            # AuthenticationSASLFinal
            self.auth.set_server_final(data[4:].decode(self._encode))

    def handle_parameter_status(self, data):
        print("handle_parameter_status", data)

    def handle_backend_key_data(self, data):
        print("handle_backend_key_data", data)

    def handle_ready_for_query(self, data):
        print("handle_ready_for_query", data)

    # def execute(self, statement):
    #     self.execute_simple(statement)

    # def execute_simple(self, statement):
    #     print("execute.statement", statement)

    #     self.send_parse(statement)

    #     self._handle_messages()

    #     self.send_describe_statement()
    #     self.send_bind()

    #     self._handle_messages()

    #     self.send_execute()

    #     self._handle_messages()

    #     return self

    # def _handle_messages(self):
    #     code = None
    #     READY_FOR_QUERY = b"Z"

    #     message_types = {
    #         b"Z": self.handle_ready_for_query,
    #         b"1": self.handle_parse_complete,
    #         b"t": self.handle_parameter_description,
    #         b"2": self.handle_bind_complete,
    #         b"C": self.handle_command_complete,
    #         b"T": self.handle_row_description,
    #         b"D": self.handle_data_row,
    #     }

    #     while code != READY_FOR_QUERY:
    #         code, data_len_with_myself = self._receive()
    #         data_len = data_len_with_myself - 4

    #         print("code", code, "data_len", data_len)

    #         message_types[code](self._read(data_len))

    # def send_parse(self, statement):
    #     print("send_parse")
    #     PARSE = b"P"
    #     oids = ()

    #     val = bytearray(self.NULL_BYTE)
    #     val.extend(statement.encode(self._encode) + self.NULL_BYTE)
    #     val.extend(Struct(f"!h").pack(len(oids)))
    #     for oid in oids:
    #         val.extend(Struct(f"!i").pack(0 if oid == -1 else oid))

    #     self._send_messages(PARSE, val)
    #     self._write_flush()
    #     self._write_sync()
    #     self._sock.flush()

    # def send_describe_statement(self):
    #     print("send_describe_statement")
    #     DESCRIBE = b"D"
    #     STATEMENT = b"S"

    #     self._send_messages(DESCRIBE, STATEMENT + self.NULL_BYTE)
    #     self._write_flush()
    #     self._write_sync()
    #     self._sock.flush()

    # def send_bind(self):
    #     print("send_bind")
    #     BIND = b"B"
    #     params = ()

    #     val = bytearray(self.NULL_BYTE + self.NULL_BYTE + Struct(f"!h").pack(0) + Struct(f"!h").pack(len(params)))

    #     for value in params:
    #         if value is None:
    #             val.extend(Struct(f"!i").pack(-1))
    #         else:
    #             val = value.encode(self._encode)
    #             val.extend(Struct(f"!i").pack(len(val)))
    #             val.extend(val)
    #     val.extend(Struct(f"!h").pack(0))

    #     self._send_messages(BIND, val)
    #     self._write_flush()
    #     self._write_sync()
    #     self._sock.flush()

    # def send_execute(self):
    #     print("send_execute")
    #     EXECUTE = b"E"
    #     data = self.NULL_BYTE + Struct(f"!i").pack(0)
    #     execute_msg = EXECUTE + Struct(f"!i").pack(len(data) + 4) + data

    #     self._write(execute_msg)
    #     self._write_flush()
    #     self._write_sync()
    #     self._sock.flush()

    # def handle_parse_complete(self, data):
    #     print("handle_parse_complete", data)

    # def handle_parameter_description(self, data):
    #     print("handle_parameter_description", data, data.decode("ascii"))

    # def handle_bind_complete(self, data):
    #     print("handle_bind_complete", data)

    # def handle_command_complete(self, data):
    #     print("handle_command_complete", data)

    # def handle_row_description(self, data):
    #     print("handle_row_description", data)
    #     count = Struct(f"!h").unpack_from(data)[0]
    #     idx = 2
    #     columns = []
    #     for i in range(count):
    #         name = data[idx : data.find(self.NULL_BYTE, idx)]
    #         idx += len(name) + 1
    #         field = dict(
    #             zip(
    #                 (
    #                     "table_oid",
    #                     "column_attrnum",
    #                     "type_oid",
    #                     "type_size",
    #                     "type_modifier",
    #                     "format",
    #                 ),
    #                 Struct(f"!ihihih").unpack_from(data, idx),
    #             )
    #         )
    #         field["name"] = name.decode(self._encode)
    #         idx += 18
    #         columns.append(field)

    #     print("columns", columns)
    #     self.columns = columns

    # def handle_data_row(self, data):
    #     print("handle_data_row", data)

    #     INTEGER = 23
    #     TEXT = 25

    #     PG_TYPES = {
    #         INTEGER: int,
    #         TEXT: str,
    #     }
    #     idx = 2
    #     row = {}
    #     for column in self.columns:
    #         vlen = Struct(f"!i").unpack_from(data, idx)[0]
    #         idx += 4
    #         if vlen == -1:
    #             v = None
    #         else:
    #             v = PG_TYPES[column["type_oid"]](str(data[idx : idx + vlen], encoding=self._encode))
    #             idx += vlen
    #         row[column["name"]] = v
    #     self.rows.append(row)

    # def fetchall(self):
    #     return self.rows


if __name__ == "__main__":
    client = Client()
    client.socket()
    client.connect()
    client.authenticate()

    # client.execute_simple("SELECT * FROM book")
    # print(client.fetchall())
