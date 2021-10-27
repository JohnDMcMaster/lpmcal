#!/usr/bin/env python3
"""
Probe Resp: 2.570E-1 A/W @ 514 nm
Probe Cal Date Sep 10 2003


mcmaster@necropolis:~/doc/ext/molectron$ hexdump -C out.bin
00000000  65 03 00 00 03 03 53 31  30 07 30 33 33 38 48 30  |e.....S10.0338H0|
00000010  33 01 30 19 30 00 00 6d  01 00 00 01 00 00 00 00  |3.0.0..m........|
00000020  00 00 c8 42 00 00 00 00  1c 00 00 00 01 3e c8 00  |...B.........>..|
00000030  00 00 d2 00 00 00 dc 00  00 00 e6 00 00 00 f0 00  |................|
00000040  00 00 fa 00 00 00 04 01  00 00 0e 01 00 00 18 01  |................|
00000050  00 00 22 01 00 00 2c 01  00 00 36 01 00 00 40 01  |.."...,...6...@.|
00000060  00 00 45 01 00 00 4a 01  00 00 54 01 00 00 5e 01  |..E...J...T...^.|
00000070  00 00 68 01 00 00 72 01  00 00 7c 01 00 00 86 01  |..h...r...|.....|
00000080  00 00 90 01 00 00 a4 01  00 00 b8 01 00 00 ba 01  |................|
00000090  00 00 cc 01 00 00 e0 01  00 00 f4 01 00 00 02 02  |................|
000000a0  00 00 08 02 00 00 1c 02  00 00 30 02 00 00 44 02  |..........0...D.|
000000b0  00 00 58 02 00 00 6c 02  00 00 79 02 00 00 80 02  |..X...l...y.....|
000000c0  00 00 94 02 00 00 a8 02  00 00 bc 02 00 00 d0 02  |................|
000000d0  00 00 e4 02 00 00 f8 02  00 00 0c 03 00 00 20 03  |.............. .|
000000e0  00 00 34 03 00 00 48 03  00 00 52 03 00 00 5c 03  |..4...H...R...\.|
000000f0  00 00 70 03 00 00 84 03  00 00 98 03 00 00 ac 03  |..p.............|
00000100  00 00 c0 03 00 00 d4 03  00 00 e8 03 00 00 fc 03  |................|
00000110  00 00 10 04 00 00 24 04  00 00 28 04 00 00 38 04  |......$...(...8.|
00000120  00 00 4c 04 00 00 01 3e  02 02 02 02 02 02 02 02  |..L....>........|
00000130  02 02 02 02 02 01 02 02  02 02 02 02 02 02 02 02  |................|
00000140  01 02 02 02 01 02 02 02  02 02 02 01 02 02 02 02  |................|
00000150  02 02 02 02 02 02 02 01  02 02 02 02 02 02 02 02  |................|
00000160  02 02 02 01 02 02 01 3e  46 25 f5 3d 24 28 fe 3d  |.......>F%.=$(.=|
00000170  ee eb 00 3e 14 3f 06 3e  a7 e8 08 3e ee eb 00 3e  |...>.?.>...>...>|
00000180  d6 56 ec 3d f2 d2 cd 3d  ce aa cf 3d 1e a7 e8 3d  |.V.=...=...=...=|
00000190  a5 bd 01 3e 02 2b 07 3e  83 c0 0a 3e 04 56 0e 3e  |...>.+.>...>.V.>|
000001a0  bc 05 12 3e 2b 18 15 3e  cf 66 15 3e 86 c9 14 3e  |...>+..>.f.>...>|
000001b0  19 04 16 3e 9b 55 1f 3e  0d 71 2c 3e c6 dc 35 3e  |...>.U.>.q,>..5>|
000001c0  cb 10 47 3e 74 b5 55 3e  3d 0a 57 3e 78 9c 62 3e  |..G>t.U>=.W>x.b>|
000001d0  c4 b1 6e 3e 12 a5 7d 3e  81 95 83 3e ef 38 85 3e  |..n>..}>...>.8.>|
000001e0  55 30 8a 3e b2 9d 8f 3e  06 81 95 3e 75 02 9a 3e  |U0.>...>...>u..>|
000001f0  ae d8 9f 3e 0a d7 a3 3e  e6 ae a5 3e 03 09 aa 3e  |...>...>...>...>|
00000200  0e 4f af 3e 21 b0 b2 3e  07 5f b8 3e ff 21 bd 3e  |.O.>!..>._.>.!.>|
00000210  f7 e4 c1 3e c2 86 c7 3e  b1 50 cb 3e 97 90 cf 3e  |...>...>.P.>...>|
00000220  4f af d4 3e 3d 0a d7 3e  9a 99 d9 3e 49 2e df 3e  |O..>=..>...>I..>|
00000230  14 d0 e4 3e f9 0f e9 3e  d6 c5 ed 3e c5 fe f2 3e  |...>...>...>...>|
00000240  45 d8 f0 3e 79 58 e8 3e  d7 12 d2 3e 71 1b ad 3e  |E..>yX.>...>q..>|
00000250  10 7a 76 3e 42 60 65 3e  57 ec 2f 3e d9 3d f9 3d  |.zv>B`e>W./>.=.=|
00000260  01 3e 00 00 80 3f 00 00  80 3f 00 00 80 3f 00 00  |.>...?...?...?..|
00000270  80 3f 00 00 80 3f 00 00  80 3f 00 00 80 3f 00 00  |.?...?...?...?..|
*
00000350  80 3f 00 00 80 3f 00 00  80 3f 00 01 00 01 00 00  |.?...?...?......|
00000360  00 61 bd 00 00 00 ff ff  ff ff ff ff ff ff ff ff  |.a..............|
00000370  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
*
00001000

"""

import argparse
import struct

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

def read_struct(buff, format):
    n = struct.calcsize(format)
    ret = struct.unpack(format, buff[0:n])
    del buff[0:n]
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

def run(fn_in):
    buff = bytearray(open(fn_in, "rb").read())
    l = read_u32(buff)
    print("Bytes: %u" % l)
    # 4 bytes already consumed
    buff = buff[0:l - 4]
    print("unknown", read_u8(buff))
    model = read_str(buff)
    print("Model: %s" % model)
    print("S/N: %s" % read_str(buff))


    # 200 to 1100 nm
    # 62 values => 3e
    # value just before this table
    buff = bytearray(open(fn_in, "rb").read())
    ncal = buff[0x2D]
    print("entries", ncal)
    nms = []
    buff = buff[0x2E:]
    print("nms")
    for _cali in range(ncal):
        nm, _x = read_struct(buff, "<HH")
        print("  ", nm)
        nms.append(nm)

    print("val", read_u8(buff))
    print("val", read_u8(buff))

    print("second")
    val2s = []
    for _cali in range(ncal):
        val2 = read_u8(buff)
        print("  ", val2)
        val2s.append(nm)

    print("val", read_u8(buff))
    print("val", read_u8(buff))

    # The two upper bytes are tracking each other
    # What about the lower two? Are they just noise?
    print("third")
    val3s = []
    for _cali in range(ncal):
        val3 = read_u32(buff)
        print("  ", val3)
        val3s.append(nm)

    print("val", read_u8(buff))
    print("val", read_u8(buff))
    print("val", read_u8(buff))
    print("val", read_u8(buff))

def main():
    parser = argparse.ArgumentParser(
        description='Decode')
    parser.add_argument('fn_in', help='File name in')
    args = parser.parse_args()
    run(fn_in=args.fn_in)

if __name__ == "__main__":
    main()
