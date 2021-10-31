#!/usr/bin/env python3

import argparse
import struct
from uvscada.util import hexdump
import datetime

def peek_u8(buff, off):
    return buff[off]

def peek_u16(buff, off):
    return struct.unpack("<H", buff[off:off+2])[0]

def peek_u32(buff, off):
    return struct.unpack("<I", buff[off:off+4])[0]

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

def decode_single(buff):
    """
    File for single wavelength correction
    All of these are J25 probes
    
    https://microwiki.org/wiki/index.php/Molectron
    
    
    j25lp-3a-050_0946e07.bin
        Peter
        Label
            Unknown
    j25lp-4_0437e03.bin
        McMaster
        BNC adapter
        Label
            1.827E+01 V/J
            248 nm
            12/08/08
        3sigma
            1.828e+1 V/J
            248 nm
    jsa-bnc_0953l05_1778c06.bin
        Peter
        Label
            Unknown
    
    
    
    
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

    0x378d/365
    38.961643835616435
    ugh
    351 remainder...
    Around Dec 16
    but maybe some rounding error there with leap years? messy
    so...1970 epoch

    (datetime.datetime(2008,12,8) - datetime.datetime(1970,1,1)).days
    14221
    0x378d
    yep! but ugh

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

    assert len(buff) == 105

    if 0:
        print("")
        hexdump(buff)
        print("")
    assert peek_u32(buff, 0x08) == 2
    print("Wavelength:", peek_u16(buff, 0x47))

def read_struct(buff, format):
    n = struct.calcsize(format)
    ret = struct.unpack(format, buff[0:n])
    del buff[0:n]
    return ret

def decode_multi(fn_in, buff):
    """
    Probe Resp: 2.570E-1 A/W @ 514 nm
    Probe Cal Date Sep 10 2003

    extract ok!
    514 1 0.25699999928474426 1065353216

    one of these has to be the cal date

    val 0x00 12313
        0x3019
        48
        25
    val 0x15 28
        0x1c
    val F 48481
        0xbd61
        189
        97


    
    
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

    if 0:
        print("")
        hexdump(buff)
        print("")

    """
    $ hexdump -C s10_0338h03.bin |head -n 2
    00000000  19 30 00 00 6d 01 00 00  01 00 00 00 00 00 00 c8  |.0..m...........|
    00000010  42 00 00 00 00 1c 00 00  00 01 3e c8 00 00 00 d2  |B.........>.....|
    $ hexdump -C op-2-vis_219708.bin |head -n 2
    00000000  1d 32 00 00 6d 01 00 00  01 00 00 00 00 00 00 80  |.2..m...........|
    00000010  3f 00 00 00 00 10 00 00  00 01 2d 90 01 00 00 95  |?.........-.....|
    $ hexdump -C op-2-ir_22045.bin |head -n 2
    00000000  24 32 00 00 6d 01 00 00  01 00 00 00 00 00 00 00  |$2..m...........|
    00000010  00 00 00 00 00 04 00 00  00 01 1e 20 03 00 00 34  |........... ...4|
    $ hexdump -C op-2-vis_0158k12r.bin |head -n 2
    00000000  29 3d 00 00 6d 01 00 00  01 00 00 00 00 00 00 80  |)=..m...........|
    00000010  3f 00 00 00 00 10 00 00  00 01 2d 90 01 00 00 95  |?.........-.....|
    """

    # print("val 0x00:", peek_u32(buff, 0x00), "/", hex(peek_u32(buff, 0x00)))
    # assert peek_u32(buff, 0x04) == 0x016D
    assert peek_u32(buff, 0x08) == 1
    assert peek_u8(buff, 0x0C) == 0
    assert peek_u8(buff, 0x0D) == 0
    assert peek_u8(buff, 0x0E) == 0
    """
    ++ ./decode_jsa.py eeprom/jsa/op-2-vis_0158k12r.bin
    val 0x15 16
    ++ ./decode_jsa.py eeprom/jsa/op-2-ir_22045.bin
    val 0x15 4
    ++ ./decode_jsa.py eeprom/jsa/s10_0338h03.bin
    val 0x15 28
    ++ ./decode_jsa.py eeprom/jsa/op-2-vis_219708.bin
    val 0x15 16
    """
    print("val 0x15:", peek_u8(buff, 0x15))
    assert peek_u8(buff, 0x19) == 1

    # 200 to 1100 nm
    # 62 values => 3e
    # value just before this table
    # buff = bytearray(open(fn_in, "rb").read())
    # 0x2D => 0x1A
    ncal = buff[0x1A]
    # print("entries", ncal)
    nms = []
    buff = buff[0x1B:]
    # print("nms")
    for _cali in range(ncal):
        nm, x1 = read_struct(buff, "<HH")
        assert x1 == 0
        # print("  ", nm)
        nms.append(nm)

    val_a = read_u8(buff)
    assert val_a == 1, val_a
    ncal2 = read_u8(buff)
    assert ncal2 == ncal, ncal2

    # print("second")
    val2s = []
    for _cali in range(ncal):
        val2 = read_u8(buff)
        """
        s10_0338h03.bin: 1 or 2
        op-2-ir_22045.bin: always 1
        op-2-vis_0158k12r.bin: always 1
        op-2-vis_219708.bin: always 1
        """
        assert val2 in (1, 2)
        # print("  ", val2)
        val2s.append(val2)

    val_c = read_u8(buff)
    assert val_c == 1, val_c
    ncal3 = read_u8(buff)
    assert ncal3 == ncal, ncal3

    # The two upper bytes are tracking each other
    # What about the lower two? Are they just noise?
    # print("third")
    val3s = []
    for _cali in range(ncal):
        # val3 = read_u32(buff)
        val3 = read_f(buff)
        """
        Most sets this is below 0.5
        op-2-ir_22045.bin however has some values approaching 1.0
        """
        assert 0.0 < val3 < 1.0
        # print("  ", val3)
        val3s.append(val3)
        # print(hex(val3))

    val_d = read_u8(buff)
    assert val_d == 1, val_d
    ncal4 = read_u8(buff)
    assert ncal4 == ncal, ncal4

    # Value seems to always be the same
    # weird
    # print("fourth")
    val4s = []
    for _cali in range(ncal):
        val4 = read_u32(buff)
        val4s.append(val4)
        # print(val4)

    """
    ++ ./decode_jsa.py eeprom/jsa/op-2-vis_0158k12r.bin
    XXX00000000  00 01 00 01 00 00 00 3B  C6 00 00                 |.......;...     |
    ++ ./decode_jsa.py eeprom/jsa/op-2-ir_22045.bin
    XXX00000000  00 01 00 01 00 00 00 AB  68 00 00                 |........h..     |
    ++ ./decode_jsa.py eeprom/jsa/s10_0338h03.bin
    XXX00000000  00 01 00 01 00 00 00 61  BD 00 00                 |.......a...     |
    ++ ./decode_jsa.py eeprom/jsa/op-2-vis_219708.bin
    XXX00000000  00 01 00 01 00 00 00 EB  CA 00 00                 |...........     |
    """
    # print("remain end", len(buff))
    assert len(buff) == 11
    
    assert read_u8(buff) == 0x00
    assert read_u8(buff) == 0x01
    assert read_u8(buff) == 0x00
    assert read_u8(buff) == 0x01
    assert read_u8(buff) == 0x00
    assert read_u8(buff) == 0x00
    assert read_u8(buff) == 0x00

    """
    ++ ./decode_jsa.py eeprom/jsa/op-2-vis_0158k12r.bin
    val F 50747
    ++ ./decode_jsa.py eeprom/jsa/op-2-ir_22045.bin
    val F 26795
    ++ ./decode_jsa.py eeprom/jsa/s10_0338h03.bin
    val F 48481
    ++ ./decode_jsa.py eeprom/jsa/op-2-vis_219708.bin
    val F 51947

    >>> struct.unpack("<f", b"\x00\x00\x3B\xC6")
    (-11968.0,)
    >>> struct.unpack("<f", b"\x00\x3B\xC6\x00")
    (1.8204593451287422e-38,)
    >>> struct.unpack("<f", b"\x3B\xC6\x00\x00")
    (7.111169316909149e-41,)
    """
    valf = read_u16(buff)
    print("val F:", valf, "/", hex(valf))
    assert read_u16(buff) == 0

    print("table (%s)" % ncal)
    for nm, val2, val3, val4 in zip(nms, val2s, val3s, val4s):
        print("  ", nm, val2, val3, val4)

def run(fn_in):
    if 0:
        float_test(fn_in)
        return

    buff = bytearray(open(fn_in, "rb").read())
    l = read_u32(buff)
    print("Bytes: %u" % l)
    # 4 bytes already consumed
    buff = buff[0:l - 4]
    cal_fmt = read_u8(buff)
    """
    2: J25
        not wavelength corrected
    3: OP-2, S10
        wavelength corrected?
    """
    cal_fmt2str = {
        2: "SINGLE",
        3: "MULTI"}
    print("Calibration format: %u (%s)" % (cal_fmt, cal_fmt2str[cal_fmt]))
    model = read_str(buff)
    print("Model: %s" % model)
    print("S/N: %s" % read_str(buff))

    # ''
    # '0'
    # '1027011'
    print("Something: ", read_str(buff))
    # Seems remainder is fixed size
    # print("Remain", len(buff))
    # open("buff.bin", "wb").write(buff)

    cal_days_1970 = peek_u32(buff, 0x00)
    cal_dt = datetime.datetime(1970,1,1) + datetime.timedelta(days=cal_days_1970)
    print("Cal date", cal_dt.strftime('%Y-%m-%d'))
    # 0x16D => 365
    # hmm date related? Expiration days?
    cal_due_days = peek_u32(buff, 0x04)
    assert cal_due_days == 0x016D
    cal_due_dt = cal_dt + datetime.timedelta(days=cal_due_days)
    print("Cal due", cal_due_dt.strftime('%Y-%m-%d'))

    if cal_fmt == 2:
        decode_single(buff)
    elif cal_fmt == 3:
        decode_multi(fn_in, buff)
    else:
        assert 0, cal_fmt


def main():
    parser = argparse.ArgumentParser(
        description='Decode')
    parser.add_argument('fn_in', help='File name in')
    args = parser.parse_args()
    run(fn_in=args.fn_in)

if __name__ == "__main__":
    main()
