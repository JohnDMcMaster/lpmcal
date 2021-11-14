#!/usr/bin/env python3
"""
Based on
https://laserpointerforums.com/threads/gentec-ps-310wb-thermopile.61640/page-3
Gentec PS-310WB Thermopile


This data includes sensitivity, model, serial number, version,
wavelength correction factors, and time response.

The DB-15 male "intelligent" connector contains an EEPROM (Electrically Erasable Programmable
Read-Only Memory) with different information such as the model of the detector, the calibration
sensitivity, the applicable scales and the wavelength correction factor for up to 20 wavelengths
related to the Ultra Series UP detector head in use.

 Pre-programmed
wavelength correction factors dedicated to each detector head are available and automatically loaded
from the detector EEPROM, for version 5 and higher detector heads. When a new detector is plugged in,
the calibration wavelength is the default selection.
"""

import argparse
import struct
from lpmcal.util import hexdump
import datetime
from lpmcal.parser import *
from lpmcal.util import tostr


def run(fn_in, verbose=False):
    print("")
    print("Reading", fn_in)

    """
    00000000  00 00 00 00 d0 e8 00 58  00 0c 00 00 e4 d8 e4 d4  |.......X........|
    00000010  00 c0 00 00 00 00 00 00  00 00 fe 00 00 4a e0 48  |.............J.H|
    00000020  00 f8 00 00 fe 00 00 00  00 00 0a f4 8e 5c 70 60  |.............\p`|
    00000030  ee 38 8a 60 4c 40 cc b4  c0 c4 08 5c 00 00 00 00  |.8.`L@.....\....|
    00000040  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    00000050  00 00 00 00 00 24 00 00  00 38 00 02 72 70 fe 4a  |.....$...8..rp.J|
    00000060  e6 04 fe 2a 74 28 fe 0a  34 6c fe 04 88 e0 fe 02  |...*t(..4l......|
    00000070  d0 74 fc fe ea 04 fc fe  9c cc fc fa 80 50 fc fa  |.t...........P..|
    00000080  b2 80 fc f8 10 a0 00 00  00 00 00 00 00 00 00 00  |................|
    00000090  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    000000a0  30 38 00 86 ae 14 00 1c  28 f4 00 00 00 18 00 00  |08......(.......|
    000000b0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    000000c0  00 00 00 00 00 00 04 ac  7c 86 e0 8c fc fa 32 fc  |........|.....2.|
    000000d0  fc f8 36 60 fc fc 20 30  fc fe 8c 64 fc fc 20 20  |..6`.. 0...d..  |
    000000e0  fe 00 00 00 fe 00 2e 3c  fe 00 e8 50 fe 04 00 02  |.......<...P....|
    000000f0  fe 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    """

    # floats: nope
    if 0:
        for ii in range(4):
            buff = bytearray(open(fn_in, "rb").read())
            # buff = buff[0x5C + ii:]
            buff = buff[0xC6 + ii:]
            hexdump(buff)
        
            for i in range(10):
                print("")
                print(i)
                # read_debug_u16be(buff)
                # read_debug_u16be(buff)
                peek_debug_fle(buff)
                read_debug_fle(buff)

    # As signed: -438 to -776
    if 0:
        buff = bytearray(open(fn_in, "rb").read())
        buff = buff[0x5C+2:]
        hexdump(buff)
    
        for i in range(10):
            print("")
            print(i)
            read_debug_u16sbe(buff)
            read_debug_u16sbe(buff)


    if 1:
        buff = bytearray(open(fn_in, "rb").read())
        while True:
            # read_debug_u16be(buff)
            read_debug_u8(buff)


def main():
    parser = argparse.ArgumentParser(description='Decode')
    parser.add_argument('--verbose', action="store_true")
    parser.add_argument('fn_in', help='File name in')
    args = parser.parse_args()
    run(fn_in=args.fn_in, verbose=args.verbose)


if __name__ == "__main__":
    main()
