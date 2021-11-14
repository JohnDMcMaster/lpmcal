#!/usr/bin/env python3
"""
Based on
http://redlum.xohp.pagesperso-orange.fr/electronics/Newport835.html#extra
"""

import argparse
import struct
from lpmcal.util import hexdump
import datetime
from lpmcal.parser import *
from lpmcal.util import tostr


def led2str(buff):
    """
    LED format: The eight bits in each byte indicate which segment of the
    LED should be turned on (1) or off (0).  The relation between the bit
    position and the segment is as follows: (note that bit 2 controls the
    decimal point to the bottom left of the digit)
    
       --3--
      |     |
      0     6
      |     |
       --4--
      |     |
      1     7
      |     |
    2  --5--
    
    For example, programming the serial number to D3h 3Bh 23h 5B would
    display 'HELP' on startup.

    """
    ret = ""
    for n in buff:
        # print(hex(n))
        ret += {
            0xC0: "1",
            0x7A: "2",
            0xF8: "3",
            0xB9: "5",
            0xBB: "6",
            0xD9: "7",
            0xEB: "8",
        }[n]
    return ret


def led2art(byte):
    def bit(n):
        if byte & (1 << n):
            return {
                0: "|",
                1: "|",
                2: ".",
                3: "-",
                4: "-",
                5: "-",
                6: "|",
                7: "|",
            }[n]
        else:
            return " "

    return """\
   %c%c%c%c%c
  %c     %c
  %c     %c
  %c     %c
   %c%c%c%c%c
  %c     %c
  %c     %c
  %c     %c
%c  %c%c%c%c%c""" % (
        bit(3),
        bit(3),
        bit(3),
        bit(3),
        bit(3),
        bit(0),
        bit(6),
        bit(0),
        bit(6),
        bit(0),
        bit(6),
        bit(5),
        bit(5),
        bit(5),
        bit(5),
        bit(5),
        bit(1),
        bit(7),
        bit(1),
        bit(7),
        bit(1),
        bit(7),
        bit(2),
        bit(5),
        bit(5),
        bit(5),
        bit(5),
        bit(5),
    )


if 0:
    print(led2art(0x7A))
    import sys
    sys.exit(1)


def decode_com(buff, verbose=False):
    buff = buff[0:0x5D0]

    verbose and hexdump(buff)
    """
    "It carries 8K bytes of data, and shares its first 1K addresses with 
    an onboard static RAM HM6514
    (that's why its first nonzero memory address is at $400)." 
    """
    for _i in range(0x400):
        # assert read_u8(buff) == 0xFF
        read_u8(buff)

    print("Detector S/N:", led2str(read_buff(buff, 4)))
    print("Attenuator S/N:", led2str(read_buff(buff, 4)))
    read_debug_u16le(buff)
    read_debug_u16le(buff)
    read_debug_u16le(buff)

    print("Start:", read_u8(buff) * 10, "nm")
    print("End:", read_u8(buff) * 10, "nm")


def decode_a5(buff, verbose=False):
    """
    http://redlum.xohp.pagesperso-orange.fr/electronics/Newport835.html#extra

    Revision A5 EPROM format summary:
    
    000h-3F0h: All FFh=255d
    400h-403h: Detector serial number (in LED format)
    404h-407h: Attenuator serial number (in LED format)
    408h-40Ah: Unknown
    40Bh-40Dh: Unknown
    40Eh     : Start wavelength (e.g. 28h=40d -> 400nm)
    40Fh     : End wavelength (e.g. 6Eh=110d -> 1100nm)
    ***A5/A6 diverges
    410h-411h: Unknown
    412h     : Exponent bias for detector without attenuator
    413h     : Exponent bias for detector with attenuator
    414h-565h: MSB of calibration coefficients (detector without
               attenuator, followed by detector with attenuator, padded
               with zeros)
    566h-567h: Unknown
    568h-6B9h: LSB of calibration coefficients (detector without
               attenuator, followed by detector with attenuator, padded
               with zeros). Start adress may vary.
    """

    decode_com(buff, verbose=verbose)
    read_debug_u16le(buff)

    exp_wo_atten = read_u8(buff)
    print("Exponent bias for detector without attenuator:", exp_wo_atten)
    # "typically = 3 for SL and 2 for IR type det"
    exp_w_atten = read_u8(buff)
    print("Exponent bias for detector with attenuator:", exp_w_atten)


def decode_a6(buff, verbose=False):
    """
    http://redlum.xohp.pagesperso-orange.fr/electronics/Newport835.html#extra

    Revision A6 EPROM format summary:
    
    000h-3F0h: All FFh=255d
    400h-403h: Detector serial number (in LED format)
    404h-407h: Attenuator serial number (in LED format)
    408h-40Ah: Unknown
    40Bh-40Dh: Unknown; these bytes repeat the 3 previous ones and it thus seems likely
                        that these two triples are associated with detector and attenuator, resp.
    40Eh     : Start wavelength (e.g. 28h=40d -> 400nm)
    40Fh     : End wavelength (e.g. 6Eh=110d -> 1100nm)
    ***A5/A6 diverges
    410h-411h: Unknown
    416h     : Exponent bias for detector without attenuator (typically = 0)
    417h     : Exponent bias for detector with attenuator    (typically = 3 for SL and 2 for IR type det)
    418h-...h: MSB of calibration coefficients (detector without
               attenuator, followed by detector with attenuator, padded
               with zeros)
    
    506h-...: LSB of calibration coefficients (detector without
               attenuator, followed by detector with attenuator, padded
               with zeros). Start adress may vary, for example it is
                often equal to 540h.
    """

    decode_com(buff, verbose=verbose)

    read_debug_u16le(buff)
    read_debug_u16le(buff)

    # ***A5/A6 diverges
    # "typically = 0"

    # hmm these seem too large
    # Exponent bias for detector without attenuator: 7
    # Exponent bias for detector with attenuator: 32

    exp_wo_atten = read_u8(buff)
    print("Exponent bias for detector without attenuator:", exp_wo_atten)
    # "typically = 3 for SL and 2 for IR type det"
    exp_w_atten = read_u8(buff)
    print("Exponent bias for detector with attenuator:", exp_w_atten)
    """
    Calibration coefficient format: The calibration coefficients are 16
    bit floating point numbers.  The two most significant bits, when added
    to the exponent bias (offset 412h and 413h), are the base 10 exponent.
    The remaining least significant 14 bits are the fractional mantissa.
    
    Interpreting the 14 LSB as a binary number B (0 to 16383), the
    relationship between the detector responsivity (R) at a given
    wavelength and the calibration coefficient is as follows:
    
    R = (B/16384) / 10^(E+bias)
    
    For example, assuming that exponent bias is 0, here are some sample
    responsivity and corresponding 16 bit calibration coefficients:
    
    500.0 mA/W = 2000h
    250.0 mA/W = 1000h
    125.0 mA/W = 0800h
    12.50 mA/W = 4800h
    1.25  mA/W = 8800h
    125.0 uA/W = C800h
    
    Note that exponents less than zero have not been tested.  The maximum
    responsivity for positive exponents is:
    
    0.9999 A/W = 3FFFh
    """

    verbose and hexdump(buff)

    # read_debug_u32(buff)
    caln = 0x8E

    c1s = []
    c2s = []
    c3s = []
    for i in range(caln):
        c1s.append(read_u8(buff))
    verbose and hexdump(buff)
    for i in range(caln):
        c2s.append(read_u8(buff))
    for i in range(12):
        assert read_u8(buff) == 0
    for i in range(caln):
        c3s.append(read_u8(buff))
    print("Cal table")
    for c1, c2, c3 in zip(c1s, c2s, c3s):
        exp = c1 >> 6
        assert c2 == 0
        n14 = ((c1 & 0x3F) << 8) + c3
        val = (n14 / 16384.) / (10**(exp + exp_wo_atten))
        if verbose:
            print("  cs", c1, c2, c3)
        print("  %0.3f" % val)

    read_debug_u16le(buff)


def run(fn_in, version=None, verbose=False):
    print("")
    print("Reading", fn_in)

    buff = bytearray(open(fn_in, "rb").read())
    # TODO: figure out a better sanity check here
    assert len(buff) >= 0x5D0

    if version is None:
        """
        Unfortunately this string field is not in 835 dumps
        00000200  01 38 31 38 2d 49 52 00  00 00 00 00 00 00 00 00  |.818-IR.........|
        """
        if len(buff) == 2048:
            raise Exception("Bare sensor cal? FIXME")
        """
        00000000  52 45 56 20 41 31 20 20  20 53 4f 46 54 57 41 52  |REV A1   SOFTWAR|
        00000010  45 20 42 59 20 54 45 44  20 48 55 42 45 52 9b 9c  |E BY TED HUBER..|
        """
        if len(buff) == 4096:
            raise Exception("GPIB ROM? Does not contain cal data")

        assert len(
            buff) == 8 * 1024, "Need full firmware for auto detect version"
        # Firmware isn't part of the cal
        # But all dumps so far include it
        """
        000006b0  00 00 00 00 00 00 00 00  00 00 ff ff 4c 50 4d 20  |............LPM |
        000006c0  52 45 56 20 41 35 20 20  20 eb c0 7a f8 d1 b9 bb  |REV A5   ..z....|
        """
        check_a5 = tostr(buff[0x6bc:0x6c6])
        """
        00000660  ff ff ff ff ff ff ff ff  4c 50 4d 20 52 45 56 20  |........LPM REV |
        00000670  41 36 20 20 20 eb c0 7a  f8 d1 b9 bb c8 fb d9 00  |A6   ..z........|
        """
        check_a6 = tostr(buff[0x668:0x672])

        if check_a5 == "LPM REV A5":
            version = "A5"
        elif check_a6 == "LPM REV A6":
            version = "A6"
        else:
            hexdump(check_a5)
            hexdump(check_a6)
            assert 0, "Failed to detect rev (wrong format?)"

    print("Decoding version", version)
    if version == "A5":
        decode_a5(buff, verbose=verbose)
    elif version == "A6":
        decode_a6(buff, verbose=verbose)
    else:
        assert 0, ("Failed to detect rev (wrong format?)", version)


def main():
    parser = argparse.ArgumentParser(description='Decode')
    parser.add_argument('--verbose', action="store_true")
    parser.add_argument('--version', default=None)
    parser.add_argument('fn_in', help='File name in')
    args = parser.parse_args()
    run(fn_in=args.fn_in, version=args.version, verbose=args.verbose)


if __name__ == "__main__":
    main()
