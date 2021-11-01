#!/usr/bin/env python3

import argparse
import struct
from uvscada.util import hexdump
import datetime


def peek_u8(buff, off):
    return buff[off]


def peek_u16(buff, off):
    return struct.unpack(">H", buff[off:off + 2])[0]


def peek_u32(buff, off):
    return struct.unpack(">I", buff[off:off + 4])[0]


def peek_f(buff, off):
    return struct.unpack(">f", buff[off:off + 4])[0]


def read_u8(buff):
    ret = buff[0]
    del buff[0]
    return ret


def read_u16(buff):
    ret = struct.unpack(">H", buff[0:2])[0]
    del buff[0:2]
    return ret


def read_u32(buff):
    ret = struct.unpack(">I", buff[0:4])[0]
    del buff[0:4]
    return ret


def read_f(buff):
    ret = struct.unpack(">f", buff[0:4])[0]
    del buff[0:4]
    return ret


def read_str_buff(buff, n):
    ret = ""
    for i in range(n):
        chari = buff[i]
        if chari:
            ret += chr(chari)
    del buff[0:n]
    return ret


def read_debug_unk32(buff, label):
    f = peek_f(buff, 0)
    u32 = read_u32(buff)
    print(label + ":", u32, "/", hex(u32), "/", f)


def peek_debug_unk32(buff, label):
    f = peek_f(buff, 0)
    u32 = peek_u32(buff, 0)
    print(label + ":", u32, "/", hex(u32), "/", f)


def read_str(buff):
    """
    First field is number chars
    """
    n = buff[0]
    del buff[0]
    ret = ""
    for _i in range(n):
        ret += chr(buff[0])
        del buff[0]
    return ret


def read_struct(buff, format):
    n = struct.calcsize(format)
    ret = struct.unpack(format, buff[0:n])
    del buff[0:n]
    return ret


def run(fn_in):
    print("")
    print("Reading", fn_in)

    buff = bytearray(open(fn_in, "rb").read())
    # Fixed size structure
    buff = buff[0:0xC8]

    """
    eeprom/lm/lm-100-qd-hd_j465.bin
    
    00000000  01 06 30 30 35 31 31 36  00 4c 4d 2d 35 30 30 30  |..005116.LM-5000|
    00000000  01 16 30 30 42 42 32 38  00 4c 4d 2d 31 30 20 51  |..00BB28.LM-10 Q|
    00000000  01 16 31 36 34 00 00 00  00 4c 4d 2d 34 35 20 51  |..164....LM-45 Q|
    00000000  01 16 31 39 5a 37 38 00  00 4c 4d 2d 31 30 20 51  |..19Z78..LM-10 Q|
    00000000  01 16 32 32 31 34 36 33  00 4c 4d 2d 33 30 56 20  |..221463.LM-30V |
    00000000  01 16 47 35 35 35 00 00  00 4c 4d 2d 31 30 20 51  |..G555...LM-10 Q|
    00000000  01 16 4a 34 35 36 00 00  00 4c 4d 2d 31 30 30 20  |..J456...LM-100 |
    00000000  01 16 43 30 34 30 00 00  00 4c 4d 2d 31 30 20 51  |..C040...LM-10 Q|
    00000000  02 08 30 31 41 5a 37 34  00 4c 4d 2d 32 20 49 52  |..01AZ74.LM-2 IR|
    00000000  02 08 30 35 30 30 48 30  00 4c 4d 2d 32 20 49 52  |..0500H0.LM-2 IR|
    00000000  02 08 30 30 58 47 36 30  00 4c 4d 2d 32 20 53 49  |..00XG60.LM-2 SI|
    00000000  02 08 31 34 33 33 44 30  00 4c 4d 2d 32 20 55 56  |..1433D0.LM-2 UV|

    hmm these are weird
    00000000  01 41 4a 4b 37 38 00 00  00 4c 4d 2d 50 31 30 46  |.AJK78...LM-P10F|
    00000000  01 41 5a 4c 30 32 00 00  00 4c 4d 2d 50 31 30 46  |.AZL02...LM-P10F|
    """

    print("Prefix1: %u" % read_u8(buff))
    print("Prefix2: %u" % read_u8(buff))
    print("Serial number: %s" % read_str_buff(buff, 7))
    print("Model number: %s" % read_str_buff(buff, 17))
    print("Part number: %s" % read_str_buff(buff, 13))


    read_debug_unk32(buff, "A")
    read_debug_unk32(buff, "B")
    read_debug_unk32(buff, "C")
    read_debug_unk32(buff, "D")
    read_debug_unk32(buff, "E")
    read_debug_unk32(buff, "F")
    read_debug_unk32(buff, "G")
    read_debug_unk32(buff, "H")
    read_debug_unk32(buff, "I")
    read_debug_unk32(buff, "J")
    print("thing: %u" % read_u8(buff))
    read_debug_unk32(buff, "K")
    read_debug_unk32(buff, "L")
    read_debug_unk32(buff, "M")

    print('loop')

    for i in range(5):
        read_debug_unk32(buff, "M")

    print('loop')

    for i in range(8):
        read_debug_unk32(buff, "M")

    print('loop')

    for i in range(8):
        read_debug_unk32(buff, "M")

    print('loop')

    for i in range(6):
        read_debug_unk32(buff, "M")

    assert len(buff) == 0

def main():
    parser = argparse.ArgumentParser(description='Decode')
    parser.add_argument('fn_in', help='File name in')
    args = parser.parse_args()
    run(fn_in=args.fn_in)

if __name__ == "__main__":
    main()
