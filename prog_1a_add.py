#!/usr/bin/env python3
# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""The first program to add two numbers in memory.

The result is stored in a third memory location.

This version uses the machine module and Computer.
"""

import sys
import machine

TITLE = 'Program 1. Add'

DATA = (
    (0x10, 0x02),
    (0x11, 0x03),
    (0x12, 0x00))

PROGRAM = (
    (0x20, 0x21),  # LDA
    (0x21, 0x10),  # 0x10
    (0x22, 0x20),  # ADD
    (0x23, 0x11),  # 0x11
    (0x24, 0x22),  # STA
    (0x25, 0x12),  # 0x12
    (0x26, 0x01),  # HLT
    (0x27, 0x00))  # (unused)


def main():
    """Run the program."""

    computer = machine.Computer(data=DATA, program=PROGRAM)
    run_flag = len(sys.argv) >= 2 and '--run' in sys.argv
    computer.run(title=TITLE, run_flag=run_flag)


if __name__ == '__main__':
    main()
