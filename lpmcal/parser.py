import struct


def peek_u8(buff, off):
    return buff[off]


def peek_u16(buff, off):
    return struct.unpack("<H", buff[off:off + 2])[0]


def peek_u32(buff, off):
    return struct.unpack("<I", buff[off:off + 4])[0]


def peek_f(buff, off):
    return struct.unpack("<f", buff[off:off + 4])[0]


def read_u8(buff):
    ret = buff[0]
    del buff[0]
    return ret


def read_u16(buff):
    ret = struct.unpack("<H", buff[0:2])[0]
    del buff[0:2]
    return ret


def read_u32(buff):
    ret = struct.unpack("<I", buff[0:4])[0]
    del buff[0:4]
    return ret


def read_f(buff):
    ret = struct.unpack("<f", buff[0:4])[0]
    del buff[0:4]
    return ret


def read_debug_unk32(buff, label):
    f = peek_f(buff, 0)
    u32 = read_u32(buff)
    print(label + ":", u32, "/", hex(u32), "/", f)
    return u32


def read_debug_u8(buff, label):
    u8 = read_u8(buff)
    print(label + ":", u8, "/", hex(u8))
    return u8


def read_debug_u16(buff, label):
    u16 = read_u16(buff)
    print(label + ":", u16, "/", hex(u16))
    return u16


def read_debug_u32(buff, label):
    u32 = read_u32(buff)
    print(label + ":", u32, "/", hex(u32))
    return u32


def read_debug_f(buff, label):
    f = read_f(buff)
    print(label + ":", f)
    return f


def peek_debug_f(buff, label):
    f = peek_f(buff, 0)
    print(label + ":", f)
    return f


def peek_debug_unk32(buff, label):
    f = peek_f(buff, 0)
    u32 = peek_u32(buff, 0)
    print(label + ":", u32, "/", hex(u32), "/", f)


def read_str_buff(buff, n):
    ret = ""
    for i in range(n):
        chari = buff[i]
        if chari:
            ret += chr(chari)
    del buff[0:n]
    return ret


def read_struct(buff, format):
    n = struct.calcsize(format)
    ret = struct.unpack(format, buff[0:n])
    del buff[0:n]
    return ret
