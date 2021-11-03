#!/usr/bin/env python3

import argparse
import struct
from uvscada.util import hexdump
import datetime


def run(fn_in, verbose=False):
    print("")
    print("Reading", fn_in)

    buff = bytearray(open(fn_in, "rb").read())


def main():
    parser = argparse.ArgumentParser(description='Decode')
    parser.add_argument('--verbose', action="store_true")
    parser.add_argument('fn_in', help='File name in')
    args = parser.parse_args()
    run(fn_in=args.fn_in, verbose=args.verbose)


if __name__ == "__main__":
    main()
