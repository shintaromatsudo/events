from struct import Struct


def _pack_funcs(fmt):
    struc = Struct(f"!{fmt}")
    return struc.pack, struc.unpack_from


i_pack, i_unpack = _pack_funcs("i")  # int
h_pack, h_unpack = _pack_funcs("h")  # short
_, ci_unpack = _pack_funcs("ci")  # char + int
_, ihihih_unpack = _pack_funcs("ihihih")  # int + short + int + short + int + short

NULL_BYTE = b"\x00"

# Message codes
# English https://www.postgresql.org/docs/current/protocol-message-formats.html
# Japanese https://www.postgresql.jp/document/15/html/protocol-message-formats.html
NOTICE_RESPONSE = b"N"
AUTHENTICATION_REQUEST = b"R"
PARAMETER_STATUS = b"S"
BACKEND_KEY_DATA = b"K"
READY_FOR_QUERY = b"Z"
ROW_DESCRIPTION = b"T"
ERROR_RESPONSE = b"E"
DATA_ROW = b"D"
COMMAND_COMPLETE = b"C"
PARSE_COMPLETE = b"1"
BIND_COMPLETE = b"2"
NO_DATA = b"n"
PARAMETER_DESCRIPTION = b"t"

QUERY = b"Q"
BIND = b"B"
PARSE = b"P"
EXECUTE = b"E"
FLUSH = b"H"
SYNC = b"S"
PASSWORD = b"p"
DESCRIBE = b"D"

STATEMENT = b"S"
PORTAL = b"P"

INTEGER = 23
TEXT = 25

PG_TYPES = {
    INTEGER: int,
    TEXT: str,
}
