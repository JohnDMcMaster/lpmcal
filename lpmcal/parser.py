import struct


def peek_u8(buff, off):
    return buff[off]


def peek_u16le(buff, off):
    return struct.unpack("<H", buff[off:off + 2])[0]


def peek_u32le(buff, off):
    return struct.unpack("<I", buff[off:off + 4])[0]


def peek_fle(buff, off):
    return struct.unpack("<f", buff[off:off + 4])[0]


def peek_u16be(buff, off):
    return struct.unpack(">H", buff[off:off + 2])[0]


def peek_u32be(buff, off):
    return struct.unpack(">I", buff[off:off + 4])[0]


def peek_fbe(buff, off):
    return struct.unpack(">f", buff[off:off + 4])[0]


def read_buff(buff, n):
    ret = buff[0:n]
    del buff[0:n]
    return ret


def read_u8(buff):
    ret = buff[0]
    del buff[0]
    return ret


def read_u16le(buff):
    ret = struct.unpack("<H", buff[0:2])[0]
    del buff[0:2]
    return ret


def read_u32le(buff):
    ret = struct.unpack("<I", buff[0:4])[0]
    del buff[0:4]
    return ret


def read_fle(buff):
    ret = struct.unpack("<f", buff[0:4])[0]
    del buff[0:4]
    return ret


def read_u16be(buff):
    ret = struct.unpack(">H", buff[0:2])[0]
    del buff[0:2]
    return ret


def read_u16sbe(buff):
    ret = struct.unpack(">h", buff[0:2])[0]
    del buff[0:2]
    return ret


def read_u32be(buff):
    ret = struct.unpack(">I", buff[0:4])[0]
    del buff[0:4]
    return ret


def read_fbe(buff):
    ret = struct.unpack(">f", buff[0:4])[0]
    del buff[0:4]
    return ret


def read_debug_unk32le(buff, label="unknown"):
    f = peek_fle(buff, 0)
    u32 = read_u32le(buff)
    print(label + ":", u32, "/", "0x%08X" % u32, "/", f)
    return u32


def read_debug_u8(buff, label="unknown"):
    u8 = read_u8(buff)
    print(label + ":", u8, "/", "0x%02X" % u8)
    return u8


def read_debug_u16le(buff, label="unknown"):
    u16 = read_u16le(buff)
    print(label + ":", u16, "/", "0x%04X" % u16)
    return u16


def read_debug_u32le(buff, label="unknown"):
    u32 = read_u32le(buff)
    print(label + ":", u32, "/", "0x%08X" % u32)
    return u32


def read_debug_fle(buff, label="unknown"):
    f = read_fle(buff)
    print(label + ":", f)
    return f

def read_debug_u16be(buff, label="unknown"):
    u16 = read_u16be(buff)
    print(label + ":", u16, "/", "0x%04X" % u16)
    return u16


def read_debug_u16sbe(buff, label="unknown"):
    u16 = read_u16sbe(buff)
    print(label + ":", u16, "/", "0x%04X" % u16)
    return u16


def read_debug_u32be(buff, label="unknown"):
    u32 = read_u32be(buff)
    print(label + ":", u32, "/", "0x%08X" % u32)
    return u32


def read_debug_fbe(buff, label="unknown"):
    f = read_fbe(buff)
    print(label + ":", f)
    return f


def peek_debug_fle(buff, label=""):
    f = peek_fle(buff, 0)
    print(label + ":", f)
    return f


def peek_debug_unk32le(buff, label=""):
    f = peek_fle(buff, 0)
    u32 = peek_u32le(buff, 0)
    print(label + ":", u32, "/", "0x%08X" % u32, "/", f)


def peek_debug_fbe(buff, label=""):
    f = peek_fbe(buff, 0)
    print(label + ":", f)
    return f


def peek_debug_unk32be(buff, label=""):
    f = peek_fbe(buff, 0)
    u32 = peek_u32be(buff, 0)
    print(label + ":", u32, "/", "0x%08X" % u32, "/", f)


def read_str_buff(buff, n):
    ret = ""
    for i in range(n):
        chari = buff[i]
        if not chari:
            break
        ret += chr(chari)
    del buff[0:n]
    return ret


def read_byte_buff(buff, n):
    ret = buff[0:n]
    del buff[0:n]
    return ret


def read_struct(buff, format):
    n = struct.calcsize(format)
    ret = struct.unpack(format, buff[0:n])
    del buff[0:n]
    return ret
