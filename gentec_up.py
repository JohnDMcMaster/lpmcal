#!/usr/bin/env python3

import argparse
import struct
from lpmcal.util import hexdump
import datetime
from lpmcal.parser import *
from lpmcal.util import tostr
import binascii


def read_pad(buff, pad, n):
    for _i in range(n):
        assert read_u8(buff) == pad


def read_expect(buff, want):
    got = read_byte_buff(buff, len(want))
    assert want == got


def read_unk_buff(buff, n):
    got = read_byte_buff(buff, n)
    hexdump(got)


def unhex(s):
    return binascii.unhexlify(s.replace(" ", ""))


def run(fn_in, version=None, verbose=False):
    print("")
    print("Reading", fn_in)

    buff = bytearray(open(fn_in, "rb").read())
    read_pad(buff, 0xCC, 4)
    read_debug_u8(buff, "A")
    read_debug_u8(buff, "B")
    read_debug_u8(buff, "C")
    read_expect(buff, unhex("00 03 00 00 00"))
    sn = read_str_buff(buff, 12)
    print("S/N:", sn)
    read_debug_fle(buff, "D")
    read_expect(buff, unhex("17 00"))
    read_debug_fle(buff, "E")
    read_debug_fle(buff, "F")
    read_debug_u16le(buff, "G")
    read_debug_fle(buff, "H")
    read_debug_u16le(buff, "I")
    read_expect(buff, unhex("6e 15 c4 3a"))
    read_debug_u16le(buff, "J")
    model = read_str_buff(buff, 32)
    print("Model:", model)
    read_expect(buff, unhex("0b 00 00 00 0f 00 00 00"))
    print("Table")
    for _i in range(10):
        print("  ", read_fle(buff))
    read_expect(buff, unhex("28 04 00 00"))
    read_expect(buff, unhex("cc" * 24))

    read_debug_fle(buff, "M")
    read_debug_fle(buff, "N")
    read_debug_u16le(buff, "O")
    read_expect(buff, unhex("01 00 07 00 01 00 00 00"))

    read_pad(buff, 0xCC, 20)

    read_debug_unk32le(buff, "P")
    print("Table")
    for _i in range(10):
        print("  ", read_fle(buff))

    read_expect(buff, unhex("00 00 00 00 00 00 00 00  00 00 00 00 00 00"))
    assert len(buff) == 0


def main():
    parser = argparse.ArgumentParser(description='Decode')
    parser.add_argument('--verbose', action="store_true")
    parser.add_argument('fn_in', help='File name in')
    args = parser.parse_args()
    run(fn_in=args.fn_in, verbose=args.verbose)


if __name__ == "__main__":
    main()
