#!/usr/bin/env python3
# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""The first program to add two numbers in memory.

The result is stored in a third memory location.
"""

import sys
import cpu
import decoder
import memory
import version

ADDR = memory.Address
VALUE = memory.Value


def setup_computer():
    """Build the computer."""

    reg = cpu.Registers()
    mem = memory.Memory()
    alu = cpu.ArithmeticLogicUnit()
    decoder_obj = decoder.Decoder(reg, mem, alu)
    clock = cpu.Clock(reg, decoder_obj)

    reg.ip = ADDR(0x20)

    return mem, clock


def store_data(mem):
    """Store our data."

    We'll add 2 + 3.

    Data will be stored starting at 0x10 and the
    answer will be stored at address 0x12.
    """

    mem.write(ADDR(0x10), VALUE(0x02))
    mem.write(ADDR(0x11), VALUE(0x03))
    mem.write(ADDR(0x12), VALUE(0x00))


def store_program(mem):
    """Store the program starting at 0x20."""

    mem.write(ADDR(0x20), VALUE(0x21))  # LDA
    mem.write(ADDR(0x21), VALUE(0x10))  # 0x10
    mem.write(ADDR(0x22), VALUE(0x20))  # ADD
    mem.write(ADDR(0x23), VALUE(0x11))  # 0x11
    mem.write(ADDR(0x24), VALUE(0x22))  # STA
    mem.write(ADDR(0x25), VALUE(0x12))  # 0x12
    mem.write(ADDR(0x26), VALUE(0x01))  # HLT
    mem.write(ADDR(0x27), VALUE(0x00))  # (unused)


def prog_display(mem):
    """Display the data and program memory."""

    return mem.display_range(ADDR(0x20), ADDR(0x28))


def data_display(mem):
    """Display the data memory."""

    return mem.display_range(ADDR(0x10), ADDR(0x13))


def main():
    """Run the program."""

    print('Simple Computer {0}\n'.format(version.VERSION))
    print('Program 1. Add')
    print()

    mem, clock = setup_computer()
    store_data(mem)
    store_program(mem)

    print('Program:\n')
    print(prog_display(mem))
    print()

    print('Data:\n')
    print(data_display(mem))
    print()

    if len(sys.argv) < 2 or sys.argv[1] != '--run':
        sys.exit(0)

    print('*** Running...\n')

    clock.run()
    print()
    print('*** Halted.')

    print()
    print('Data:\n')
    print(data_display(mem))
    print()


if __name__ == '__main__':
    main()
