#!/usr/bin/env python3
"""
Responsivity
1.828e+1 V/J
Cal: 248 nm

COHERENT
Model: J25LP-4

COHERENT CALIBRATION TAG
DATE CALIB 12/08/08
TECH KH
NEXT DUE 12/08/09
Item #: 0010-8145
Serial #: 0437E03




Probe Resp: 1.827E+01 V/J @ 248 nm
    248 => f8
    appears once below
    
    what about Q format?

Probe Cal Date Dec 8 2008
    2008 => 0x7d8
    
    8d 37
    ?


00000000  7f 00 00 00 02 07 4a 32  35 4c 50 2d 34 07 30 34  |......J25LP-4.04|
00000010  33 37 45 30 33 00 8d 37  00 00 6d 01 00 00 02 00  |37E03..7..m.....|
00000020  00 00 06 69 fc 72 00 00  00 00 93 1a da 37 83 a5  |...i.r.......7..|
00000030  3a 39 83 a5 ba 38 00 00  00 00 00 00 00 00 00 00  |:9...8..........|
00000040  c0 41 00 00 c8 42 00 00  00 00 00 00 00 00 00 00  |.A...B..........|
00000050  00 20 41 00 00 7a 44 00  00 00 00 01 01 f8 00 00  |. A..zD.........|
00000060  00 01 01 01 01 01 33 33  92 41 01 01 dd 2e fc 72  |......33.A.....r|
00000070  00 01 00 01 00 00 00 00  00 80 3f d5 14 00 00 ff  |..........?.....|
00000080  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
*
00000f90  ff ff ff ff ff ff ff ff  ff ff ff 0f ff ff ff ff  |................|
00000fa0  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
*
00001000
"""

import argparse
import struct

def read_u8(buff):
    ret = buff[0]
    del buff[0]
    return ret

def read_u32(buff):
    ret = struct.unpack("<I", buff[0:4])[0]
    del buff[0:4]
    return ret

def read_f(buff):
    ret = struct.unpack(">f", buff[0:4])[0]
    del buff[0:4]
    return ret

def read_str_endi(buff, endi):
    ret = ""
    while True:
        i = buff[0]
        del buff[0]
        if i == endi:
            return ret
        c = chr(i)
        ret += c

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

def float_test(fn_in):
    # ./decode_j25.py j25lp-4_0437e03.bin |grep 828
    # nope
    
    for i in range(0x100):
        print("")
        print(i)
        buff = bytearray(open(fn_in, "rb").read())
        
        buff = buff[i:]
        print("%f" % struct.unpack("<e", buff[0:2])[0])
        print("%f" % struct.unpack(">e", buff[0:2])[0])
        print("%f" % struct.unpack("<f", buff[0:4])[0])
        print("%f" % struct.unpack(">f", buff[0:4])[0])
        print("%f" % struct.unpack("<d", buff[0:8])[0])
        print("%f" % struct.unpack(">d", buff[0:8])[0])

def run(fn_in):
    if 0:
        float_test(fn_in)
        return



    buff = bytearray(open(fn_in, "rb").read())
    l = read_u32(buff)
    print("Bytes: %u" % l)
    # 4 bytes already consumed
    buff = buff[0:l - 4]
    print("unknown", read_u8(buff))
    model = read_str(buff)
    print("Model: %s" % model)
    print("S/N: %s" % read_str(buff))

def main():
    parser = argparse.ArgumentParser(
        description='Decode')
    parser.add_argument('fn_in', help='File name in')
    args = parser.parse_args()
    run(fn_in=args.fn_in)

if __name__ == "__main__":
    main()
