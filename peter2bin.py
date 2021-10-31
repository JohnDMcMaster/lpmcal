#!/usr/bin/env python3

"""
Sample file:

Initialized
dumping EEPROM
{
0x01, 0x16, 0x30, 0x30, 0x42, 0x42, 0x32, 0x38, 0x00, 0x4c, 0x4d, 0x2d, 0x31, 0x30, 0x20, 0x51,
0x55, 0x41, 0x44, 0x20, 0x48, 0x44, 0x20, 0x2f, 0x31, 0x00, 0x30, 0x32, 0x31, 0x30, 0x2d, 0x38,
0x30, 0x30, 0x2d, 0x39, 0x39, 0x00, 0x00, 0x81, 0xe4, 0x81, 0xe4, 0x3b, 0x54, 0xcb, 0x9e, 0x3b,
...
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}
000: 01 16 30 30 42 42 32 38  00 4c 4d 2d 31 30 20 51  |..00BB28.LM-10 Q|
010: 55 41 44 20 48 44 20 2f  31 00 30 32 31 30 2d 38  |UAD HD /1.0210-8|
...
1d0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
1e0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
1f0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|








Initialized
dumping EEPROM
{
0x1be4, 0x0b00, 0x1751, 0xf906, 0x0a07, 0x06ff, 0x00f8, 0x300d,
...
0x03e8, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0x3858,
}

000: 1be4 0b00 1751 f906  0a07 06ff 00f8 300d  |  7140   2816   5969  -1786   2567   1791    248  12301 |
...
038: 03e8 ffff ffff ffff  ffff ffff ffff 3858  |  1000     -1     -1     -1     -1     -1     -1  14424 |
"""


import argparse
import struct
import re

def parse_curly_block(fn_in):
    f_in = open(fn_in, "r")
    ret = bytearray()

    # Find opening curly
    for l in f_in:
        if l.strip() == '{':
            break

    for l in f_in:
        """
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}
        """
        bytes = l.replace('}', '').strip()
        #print(bytes)
        #print(len(bytes))
        # 2 byte word
        for word in bytes.split(','):
            word = word.strip()
            if not word:
                continue
            if len(word) == 4:
                # 0x41
                ret += bytearray([int(word, 0)])
            else:
                # 0x1be4
                assert len(word) == 6
                # big endian
                ret += bytearray([int(word[2:4], 16)])
                ret += bytearray([int(word[4:6], 16)])
        if '}' in l:
            break
    return ret

def parse_hexdump_block(fn_in):
    f_in = open(fn_in, "r")
    assert 0

def run(fn_in, fn_out):
    print("Reading", fn_in)
    buff_curly = parse_curly_block(fn_in)
    print("Writing ", fn_out)
    f_out = open(fn_out, "wb")
    f_out.write(buff_curly)

def main():
    parser = argparse.ArgumentParser(
        description='Decode')
    parser.add_argument('fn_in', help='File name in')
    parser.add_argument('fn_out', nargs='?', help='File name in')
    args = parser.parse_args()
    fn_out = args.fn_out
    if not fn_out:
        fn_out = args.fn_in.replace('.txt', '.bin')
        assert fn_out != args.fn_in
    run(fn_in=args.fn_in, fn_out=fn_out)

if __name__ == "__main__":
    main()
