import socket

import scramp
from constants import (
    AUTHENTICATION_REQUEST,
    BACKEND_KEY_DATA,
    BIND,
    BIND_COMPLETE,
    COMMAND_COMPLETE,
    DATA_ROW,
    DESCRIBE,
    ERROR_RESPONSE,
    EXECUTE,
    FLUSH,
    NO_DATA,
    NOTICE_RESPONSE,
    NULL_BYTE,
    PARAMETER_DESCRIPTION,
    PARAMETER_STATUS,
    PARSE,
    PARSE_COMPLETE,
    PASSWORD,
    PG_TYPES,
    QUERY,
    READY_FOR_QUERY,
    ROW_DESCRIPTION,
    STATEMENT,
    SYNC,
    ci_unpack,
    h_pack,
    h_unpack,
    i_pack,
    i_unpack,
    ihihih_unpack,
)
from cursor import Cursor


class Connection:
    def __init__(self, user, host, port, database, password, timeout) -> None:
        self._encode = "utf8"

        self.user = user.encode(self._encode)
        self.database = database.encode(self._encode)
        self.password = password.encode(self._encode)

        self.rows = []
        self.columns = []
        self.error = None

        # https://www.postgresql.org/docs/current/protocol-flow.html
        # https://www.postgresql.jp/document/15/html/protocol-flow.html
        self._socket(host, port, timeout)
        self._connect()
        self._authenticate()

    def _socket(self, host, port, timeout):
        self.sock = socket.create_connection((host, port), timeout)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self._sock = self.sock.makefile("rwb")

    def _connect(self):
        # Protocol version number. Version 3.0.
        protocol = 196608
        init_val = bytearray(i_pack(protocol))

        init_val.extend("user".encode("ascii") + NULL_BYTE + self.user + NULL_BYTE)
        init_val.extend("database".encode("ascii") + NULL_BYTE + self.database + NULL_BYTE)
        init_val.extend(NULL_BYTE)

        # Message length, including itself.
        self._write(i_pack(len(init_val) + 4))
        self._write(init_val)
        self._flush()

    def _authenticate(self):
        try:
            # 1 Authentication
            # 2 ParameterStatus
            # 3 BackendKeyData
            # 4 ReadyForQuery
            self._handle_messages()
        except Exception as e:
            self.close()
            raise e

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self._sock.close()

    def cursor(self):
        return Cursor(self)

    def commit(self):
        self.execute("commit")

    def execute(self, statement, args=None):
        self.execute_simple(statement)

    def execute_simple(self, statement):
        print("execute_simple", statement)
        self.send_query(statement)
        self._handle_messages()

        return self

    def execute_extended(self, statement):
        print("execute_extended", statement)

        self.send_parse(NULL_BYTE, statement)

        self._handle_messages()

        self.send_describe_statement(NULL_BYTE)
        self.send_bind(NULL_BYTE, ())

        self._handle_messages()

        self.send_execute()

        self._handle_messages()

        return self

    def fetchall(self):
        return self.rows

    def _handle_messages(self):
        """
        https://www.postgresql.org/docs/current/protocol-message-formats.html
        https://www.postgresql.jp/document/15/html/protocol-message-formats.html
        """
        message_types = {
            AUTHENTICATION_REQUEST: self.handle_authentication_request,  # b'R'
            PARAMETER_STATUS: self.handle_parameter_status,  # b'S'
            BACKEND_KEY_DATA: self.handle_backend_key_data,  # b'K'
            READY_FOR_QUERY: self.handle_ready_for_query,  # b'Z'
            PARSE_COMPLETE: self.handle_parse_complete,  # b'1'
            PARAMETER_DESCRIPTION: self.handle_parameter_description,  # b't'
            BIND_COMPLETE: self.handle_bind_complete,  # b'2'
            COMMAND_COMPLETE: self.handle_command_complete,  # b'C'
            ROW_DESCRIPTION: self.handle_row_description,  # b'T'
            DATA_ROW: self.handle_data_row,  # b'D'
            NO_DATA: self.handle_no_data,  # b'n'
            NOTICE_RESPONSE: self.handle_notice_response,  # b'N'
            ERROR_RESPONSE: self.handle_error_response,  # b'E'
        }

        code = None
        while code != READY_FOR_QUERY:
            code, data_len_with_myself = self._receive_head()
            data_len = data_len_with_myself - 4
            data = self._read(data_len)

            print("code", code, "data_len", data_len)

            message_types[code](data)

        if self.error is not None:
            raise self.error

    def _receive_head(self):
        code, data_len_with_myself = ci_unpack(self._read(5))
        return code, data_len_with_myself

    def _send_messages(self, code, data):
        self._write(code)
        self._write(i_pack(len(data) + 4))
        self._write(data)

    def _flush(self):
        try:
            self._sock.flush()
        except OSError as e:
            raise Exception("network error") from e

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
        flush_msg = FLUSH + i_pack(4)
        self._write(flush_msg)

    def _write_sync(self):
        sync_msg = SYNC + i_pack(4)
        self._write(sync_msg)

    def _write_execute(self):
        data = NULL_BYTE + i_pack(0)
        execute_msg = EXECUTE + i_pack(len(data) + 4) + data
        self._write(execute_msg)

    def _write_flush_sync(self):
        self._write_flush()
        self._write_sync()
        self._flush()

    ### HANDLE ###
    def handle_authentication_request(self, data):
        print("handle_authentication_request")
        auth_code = i_unpack(data)[0]
        print("auth_code", auth_code)
        if auth_code == 0:
            pass

        elif auth_code == 10:
            # AuthenticationSASL
            mechanisms = [m.decode("ascii") for m in data[4:-2].split(NULL_BYTE)]

            self.auth = scramp.ScramClient(
                mechanisms,
                self.user.decode(self._encode),
                self.password.decode(self._encode),
                channel_binding=None,
            )

            init = self.auth.get_client_first().encode(self._encode)
            print("init", init)
            mech = self.auth.mechanism_name.encode("ascii") + NULL_BYTE

            # SASLInitialResponse
            self._send_messages(PASSWORD, mech + i_pack(len(init)) + init)
            self._flush()

        elif auth_code == 11:
            # AuthenticationSASLContinue
            self.auth.set_server_first(data[4:].decode(self._encode))

            # SASLResponse
            msg = self.auth.get_client_final().encode(self._encode)
            self._send_messages(PASSWORD, msg)
            self._flush()

        elif auth_code == 12:
            # AuthenticationSASLFinal
            self.auth.set_server_final(data[4:].decode(self._encode))

    def handle_parameter_status(self, data):
        """
        このメッセージは、フロントエンドに現在（初期）のclient_encodingやDateStyleなどのバックエンドパラメータの設定情報を通知します。
        フロントエンドはこのメッセージを無視しても、将来の使用に備えてその設定を記録しても構いません。
        詳細は項46.2.6を参照してください。 フロントエンドはこのメッセージに応答してはいけませんが、ReadyForQueryメッセージの監視を続けなくてはなりません。
        """
        print("handle_parameter_status", data, data.decode("ascii"))

    def handle_backend_key_data(self, data):
        """
        このメッセージは、フロントエンドがキャンセル要求を後で送信できるようにしたい場合に保存しなければならない、秘密キーデータを用意します。
        フロントエンドはこのメッセージに応答してはいけませんが、ReadyForQueryメッセージの監視を続けなくてはなりません。
        """
        print("handle_backend_key_data", data)

    def handle_ready_for_query(self, data):
        print("handle_ready_for_query", data)

    def handle_parse_complete(self, data):
        print("handle_parse_complete", data)

    def handle_parameter_description(self, data):
        print("handle_parameter_description", data, data.decode("ascii"))

    def handle_bind_complete(self, data):
        print("handle_bind_complete", data)

    def handle_command_complete(self, data):
        print("handle_command_complete", data)

    def handle_row_description(self, data):
        """
        SELECTやFETCHなどの問い合わせの応答の行がまさに返されようとしていることを示します。
        このメッセージには、行の列レイアウトに関する説明が含まれます。
        このメッセージの後に、フロントエンドに返される各行に対するDataRowメッセージが続きます。
        """
        print("handle_row_description", data)
        count = h_unpack(data)[0]  # (2,)
        idx = 2
        columns = []
        for i in range(count):
            name = data[idx : data.find(NULL_BYTE, idx)]
            idx += len(name) + 1
            field = dict(
                zip(
                    ("table_oid", "column_attrnum", "type_oid", "type_size", "type_modifier", "format"),
                    ihihih_unpack(data, idx),
                )
            )
            field["name"] = name.decode(self._encode)
            idx += 18
            columns.append(field)

        self.columns = columns

    def handle_data_row(self, data):
        """
        SELECTやFETCHなどの問い合わせで返される行の集合の1つです。
        """
        print("handle_data_row", data)
        INTEGER = 23
        TEXT = 25
        PG_TYPES = {INTEGER: int, TEXT: str}

        idx = 2
        row = {}
        for column in self.columns:
            vlen = i_unpack(data, idx)[0]
            idx += 4
            if vlen == -1:
                v = None
            else:
                v = PG_TYPES[column["type_oid"]](str(data[idx : idx + vlen], encoding=self._encode))
                idx += vlen
            row[column["name"]] = v
        self.rows.append(row)

    def handle_no_data(self, msg):
        print("handle_no_data", msg)

    def handle_notice_response(self, data):
        print("handle_notice_response", data)

    def handle_error_response(self, data):
        print("handle_error_response")
        msg = {s[:1].decode("ascii"): s[1:].decode(self._encode, errors="replace") for s in data.split(NULL_BYTE) if s != b""}

        self.error = Exception(msg)

    ### SEND ###
    def send_query(self, statement):
        print("send_query")
        self._send_messages(QUERY, statement.encode(self._encode) + NULL_BYTE)
        self._flush()

    def send_parse(self, statement_name_bin, statement, oids=()):
        print("send_parse")
        val = bytearray(statement_name_bin)
        val.extend(statement.encode(self._encode) + NULL_BYTE)
        val.extend(h_pack(len(oids)))
        for oid in oids:
            val.extend(i_pack(0 if oid == -1 else oid))

        self._send_messages(PARSE, val)
        self._write_flush_sync()

    def send_describe_statement(self, statement_name_bin):
        print("send_describe_statement")
        self._send_messages(DESCRIBE, STATEMENT + statement_name_bin)
        print(DESCRIBE, STATEMENT + statement_name_bin)
        self._write_flush_sync()

    def send_bind(self, statement_name_bin, params):
        print("send_bind")
        val = bytearray(NULL_BYTE + statement_name_bin + h_pack(0) + h_pack(len(params)))

        for value in params:
            if value is None:
                val.extend(i_pack(-1))
            else:
                val = value.encode(self._encode)
                val.extend(i_pack(len(val)))
                val.extend(val)
        val.extend(h_pack(0))

        self._send_messages(BIND, val)
        self._write_flush()

    def send_execute(self):
        print("send_execute")
        self._write_execute()
        self._write_flush_sync()
