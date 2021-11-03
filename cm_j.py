#!/usr/bin/env python3

import argparse
import struct
from uvscada.util import hexdump
import datetime
from lpmcal.parser import *


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


def decode_pyro_prefix(buff, verbose=False):
    """
    Think this is shared structure but not sure
    """

    verbose and print("prefix")
    verbose and hexdump(buff[0:38 + 16 + 4])

    read_debug_u16(buff, "pprefix-AA1")
    # 72FC
    assert read_debug_u16(buff, "pprefix-AA2")
    """
    eeprom/jsa/j-25mb-he_0984e07r.bin
    pprefix-A: 0.0005000000237487257
    pprefix-B: 4.8000001697801054e-05
    pprefix-C: 0.00018099999579135329
    pprefix-D: 9.100000170292333e-05
    pprefix-G: 22.299999237060547
    pprefix-F: 100.0

    eeprom/jsa/j25lp-4_0437e03.bin
    pprefix-A: 0.0
    pprefix-B: 2.5999999706982635e-05
    pprefix-C: 0.00017800000205170363
    pprefix-D: 8.900000102585182e-05
    pprefix-G: 24.0
    pprefix-F: 100.0
    """
    # Tricky
    # Sometimes a reasonable float like 0.0005, sometimes large constant
    # Might need more special casing
    # float, 0.0005
    read_debug_f(buff, "pprefix-A")
    # Probalby float
    read_debug_f(buff, "pprefix-B")
    # Probalby float
    read_debug_f(buff, "pprefix-C")
    # Probalby float
    read_debug_f(buff, "pprefix-D")

    assert read_u32(buff) == 0
    assert read_u32(buff) == 0
    # 22.3
    read_debug_f(buff, "pprefix-G")

    assert read_debug_f(buff, "pprefix-F") == 100.0
    assert read_u16(buff) == 0
    """
    eeprom/jsa/j25lp-3a-050_0946e07.bin
    pprefix-12: 16256 / 0x3f80
    pprefix-13: 0 / 0x0 / 0.0
    pprefix-14: 16672 / 0x4120
    pprefix-15: 17530 / 0x447a
    pprefix-16: 0 / 0x0

    eeprom/jsa/j25lp-4_0437e03.bin
    pprefix-12: 0 / 0x0
    pprefix-13: 0 / 0x0 / 0.0
    pprefix-14: 16672 / 0x4120
    pprefix-15: 17530 / 0x447a
    pprefix-16: 0 / 0x0

    eeprom/jsa/j-25mb-he_0984e07r.bin
    pprefix-12: 0 / 0x0
    pprefix-13: 0 / 0x0 / 0.0
    pprefix-14: 16672 / 0x4120
    pprefix-15: 0 / 0x0
    pprefix-16: 10 / 0xa
    """

    assert read_u8(buff) == 0
    # Sometimes 0, sometimes value
    # pprefix-2: 16256 / 0x3f80
    read_debug_u32(buff, "pprefix-12")
    assert read_debug_unk32(buff, "pprefix-13") == 0

    assert read_debug_u32(buff, "pprefix-14") == 0x4120
    # observed: 0, large value
    read_debug_u16(buff, "pprefix-15")
    # Possibly flags related to whether cal table vs single value follows
    read_debug_u32(buff, "pprefix-16")
    assert read_u8(buff) == 1


def decode_pyro_postfix(buff, verbose=False):
    verbose and print("remain end", len(buff))
    assert len(buff) == 15

    verbose and hexdump(buff)
    """
    00000000  00 01 00 01 00 00 00 00  00 80 3F 1C B0 00 00     |..........?.... |
    00000000  00 01 00 01 00 00 00 00  00 80 3F D5 14 00 00     |..........?.... |
    """

    assert read_u8(buff) == 0x00
    assert read_u8(buff) == 0x01
    assert read_u8(buff) == 0x00
    assert read_u8(buff) == 0x01
    assert read_u8(buff) == 0x00
    assert read_u8(buff) == 0x00
    assert read_u8(buff) == 0x00

    assert read_u16(buff) == 0
    read_debug_u16(buff, "ppostfix 8")
    read_debug_u16(buff, "ppostfix 9")
    assert read_u16(buff) == 0


def decode_pyro_single(buff, verbose=False):
    """
    About 64 bytes to nm bit
    use this as rough comparison to other sections

    j25lp-4_0437e03.bin
    00000000  02 00 00 00 06 69 FC 72  00 00 00 00 93 1A DA 37  |.....i.r.......7|
    00000010  83 A5 3A 39 83 A5 BA 38  00 00 00 00 00 00 00 00  |..:9...8........|
    00000020  00 00 C0 41 00 00 C8 42  00 00 00 00 00 00 00 00  |...A...B........|
    00000030  00 00 00 20 41 00 00 7A  44 00 00 00 00 01 01 F8  |... A..zD.......|

    j25lp-3a-050_0946e07.bin
    00000000  02 00 00 00 42 60 E5 3B  00 00 00 00 2C 70 93 36  |....B`.;....,p.6|
    00000010  99 06 0F 39 99 06 8F 38  00 00 00 00 00 00 00 00  |...9...8........|
    00000020  9A 99 B1 41 00 00 C8 42  00 00 00 80 3F 00 00 00  |...A...B....?...|
    00000030  00 00 00 20 41 00 00 7A  44 00 00 00 00 01 01 14  |... A..zD.......|

    j8lp-1373_0953l05.bin
    00000000  02 00 00 00 06 69 FC 72  00 00 00 00 3E 5E A3 38  |.....i.r....>^.8|
    00000010  4B 78 1D 3A 95 71 9D 39  00 00 00 00 00 00 00 00  |Kx.:.q.9........|
    00000020  CD CC B8 41 00 00 C8 42  00 00 00 80 3F 00 00 00  |...A...B....?...|
    00000030  00 00 00 20 41 00 00 A6  43 00 00 00 00 01 01 28  |... A...C......(|

    """
    # s0 = len(buff)
    # hexdump(buff[0:64])

    assert len(buff) == 93, len(buff)

    if 0:
        print("")
        hexdump(buff)
        print("")
    """
    Probe Resp: 1.827E+01 V/J @ 248 nm
    val K: 18.274999618530273

    j25lp-3a-050_0946e07.bin
    
    both of these the same:
    j25lp-4_0437e03.bin
    j8lp-1373_0953l05.bin
    
    hmm
    """
    def decode_main():
        assert read_u8(buff) == 1

        # Roughly this is where previous tables end
        # lets check before here

        # print("single: consumed %u bytes" % (s0 - len(buff)))

        nm = read_u16(buff)
        print("nm:", nm)

        assert read_u8(buff) == 0
        assert read_u8(buff) == 0
        assert read_u8(buff) == 1

        assert read_u8(buff) == 1
        assert read_u8(buff) == 1
        assert read_u8(buff) == 1
        assert read_u8(buff) == 1

        # ****
        # this is the main response value
        valk = read_f(buff)
        print("Probe Resp:", valk, "V/J")

        assert read_u8(buff) == 1
        assert read_u8(buff) == 1

        # read_debug_unk32(buff, "pyro misc")
        read_debug_u16(buff, "pyro misc1")
        # 72FC
        read_debug_u16(buff, "pyro misc2")

    decode_pyro_prefix(buff, verbose=verbose)
    decode_main()
    decode_pyro_postfix(buff, verbose=verbose)


def decode_pyro_multi(buff, verbose=False):
    """
    Table header: 62 bytes
    This is way bigger than multi1
    It is plausibly the same format as the single header, but I haven't matched it yet
    However the table itself is similar
    Ex: 20 41 appears in both

    j-25mb-he_0984e07r.bin
    00000000  02 00 00 00 00 00 80 3F  6F 12 03 3A 9C 53 49 38  |.......?o..:.SI8|
    00000010  D1 CA 3D 39 41 D7 BE 38  00 00 00 00 00 00 00 00  |..=9A..8........|
    00000020  66 66 B2 41 00 00 C8 42  00 00 00 00 00 00 00 00  |ff.A...B........|
    00000030  00 00 00 20 41 00 00 00  00 0A 00 00 00 01        |... A.........  |
    """

    # hexdump(buff[0:62])

    # s0 = len(buff)

    decode_pyro_prefix(buff)
    cals = read_multi_tables(buff)
    decode_pyro_postfix(buff)

    print("table (%s)" % len(cals))
    for nm, val2, val3, val4 in cals:
        print("  ", nm, val2, val3, val4)
        # Widest range observed: 193 nm to 14 um
        assert 10 < nm < 50000
        assert 0.0 < val3 < 10.0


def read_multi_tables(buff):
    ncal = read_u8(buff)

    nms = []
    for _cali in range(ncal):
        nms.append(read_struct(buff, "<I")[0])

    val_a = read_u8(buff)
    assert val_a == 1, val_a
    ncal2 = read_u8(buff)
    assert ncal2 == ncal, ncal2

    val2s = []
    for _cali in range(ncal):
        val2 = read_u8(buff)
        assert val2 in (1, 2)
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
        # XXX: 1065353216 / 0x3f800000 / 1.0
        # peek_debug_unk32(buff, "XXX")

        val4 = read_f(buff)
        val4s.append(val4)

    ret = []
    for nm, val2, val3, val4 in zip(nms, val2s, val3s, val4s):
        ret.append((nm, val2, val3, val4))
    return ret


def decode_semi_multi(buff, verbose=False):
    def read_prefix():
        # Table header: 18 bytes
        # s0 = len(buff)
        """
        s10_0338h03.bin
        00000000  01 00 00 00 00 00 00 C8  42 00 00 00 00 1C 00 00  |........B.......|
        00000010  00 01
    
        op-2-ir_22045.bin
        00000000  01 00 00 00 00 00 00 00  00 00 00 00 00 04 00 00  |................|
        00000010  00 01                                             |..              |
    
        op-2-vis_0158k12r.bin
        00000000  01 00 00 00 00 00 00 80  3F 00 00 00 00 10 00 00  |........?.......|
        00000010  00 01                                             |..              |
    
        op-2-vis_219708.bin
        00000000  01 00 00 00 00 00 00 80  3F 00 00 00 00 10 00 00  |........?.......|
        00000010  00 01                                             |..              |
        """
        verbose and hexdump(buff[0:14])

        assert read_u16(buff) == 0
        assert read_u8(buff) == 0

        read_debug_u16(buff, "sprefix-3")
        assert read_u32(buff) == 0
        read_debug_u32(buff, "sprefix-5")
        assert read_u8(buff) == 1

        # print("multi1: consumed %u bytes" % (s0 - len(buff)))

    def read_postfix():
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
        read_debug_u16(buff, "spostfix-8")
        assert read_u16(buff) == 0

    read_prefix()
    cals = read_multi_tables(buff)
    read_postfix()

    print("table (%s)" % len(cals))
    for nm, val2, val3, val4 in cals:
        print("  ", nm, val2, val3, val4)
        assert 10 < nm < 2000
        assert 0.0 < val3 < 1.0


def run(fn_in, verbose=False):
    print("")
    print("Reading", fn_in)
    if 0:
        float_test(fn_in)
        return

    buff = bytearray(open(fn_in, "rb").read())
    l = read_u32(buff)
    # print("Bytes: %u" % l)
    # 4 bytes already consumed
    buff = buff[0:l - 4]
    sensor_type = read_u8(buff)
    """
    2: J25
        not wavelength corrected
    3: OP-2, S10
        wavelength corrected?
    """
    cal_fmt2str = {
        # Pyroelectric
        # Usually calibrated for single wavelength
        2: "PYRO",
        # Semiconductor
        # Usually calibrated for a range of wavelengths
        3: "SEMI"
    }
    print("Sensor type: %u (%s)" % (sensor_type, cal_fmt2str[sensor_type]))
    model = read_str(buff)
    print("Model: %s" % model)
    print("S/N: %s" % read_str(buff))

    # ''
    # '0'
    # '1027011'
    print("A string: ", read_str(buff))
    # Seems remainder is fixed size
    # print("Remain", len(buff))
    # open("buff.bin", "wb").write(buff)

    cal_days_1970 = read_u32(buff)
    cal_dt = datetime.datetime(1970, 1,
                               1) + datetime.timedelta(days=cal_days_1970)
    print("Cal date", cal_dt.strftime('%Y-%m-%d'))
    # 0x16D => 365
    # hmm date related? Expiration days?
    cal_due_days = read_u32(buff)
    assert cal_due_days == 0x016D
    cal_due_dt = cal_dt + datetime.timedelta(days=cal_due_days)
    print("Cal due", cal_due_dt.strftime('%Y-%m-%d'))

    const23 = read_debug_u32(buff, "const23")

    # multi1 and multi2 seem to have different header/footer structures
    # ex: a float that clearly decodes in one doesn't in the other
    # however data representation is similar in how they store tables and such

    # Sensor type 2
    if sensor_type == 2:
        assert const23 == 2
        if model == "J-25MB-HE":
            decode_pyro_multi(buff, verbose=verbose)
        else:
            decode_pyro_single(buff, verbose=verbose)
    elif sensor_type == 3:
        assert const23 == 1
        decode_semi_multi(buff, verbose=verbose)
    else:
        assert 0, sensor_type
    assert len(buff) == 0


def main():
    parser = argparse.ArgumentParser(description='Decode')
    parser.add_argument('--verbose', action="store_true")
    parser.add_argument('fn_in', help='File name in')
    args = parser.parse_args()
    run(fn_in=args.fn_in, verbose=args.verbose)


if __name__ == "__main__":
    main()
