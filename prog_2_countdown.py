#!/usr/bin/env python3
# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""The second program that counts down from 10.x

The count will be in the accumulator.  This program displays
the address executed and also the current accumulator value
on each fetch-execute cycle.

We store a value of -1 into a memory location and then add that
location to the accumulator to decrement the value.

Also the just-added skip on zero is used to skip the jump to the
start of the loop address when the accumulator reaches zero.
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

    mem.write(ADDR(0x10), VALUE(-0x01))  # -1  ; To decrement the count.
    mem.write(ADDR(0x11), VALUE(0x0a))   # 10  ; The initial count.


def store_program(mem):
    """Store the program starting at 0x20."""

    mem.write(ADDR(0x20), VALUE(0x21))  # LDA
    mem.write(ADDR(0x21), VALUE(0x11))  # 0x11
    mem.write(ADDR(0x22), VALUE(0x20))  # ADD     ; Decrement with...
    mem.write(ADDR(0x23), VALUE(0x10))  # 0x10    ; -1
    mem.write(ADDR(0x24), VALUE(0x24))  # SZA     ; Skip if zero.
    mem.write(ADDR(0x25), VALUE(0x00))  # (unused)
    mem.write(ADDR(0x26), VALUE(0x23))  # JMP     ; Jump back to...
    mem.write(ADDR(0x27), VALUE(0x22))  # 0x22    ; loop start.
    mem.write(ADDR(0x28), VALUE(0x01))  # HLT     ; Skip to here when done.
    mem.write(ADDR(0x29), VALUE(0x00))  # (unused)


def prog_display(mem):
    """Display the data and program memory."""

    return mem.display_range(ADDR(0x20), ADDR(0x2a))


def data_display(mem):
    """Display the data memory."""

    return mem.display_range(ADDR(0x10), ADDR(0x12))


def main():
    """Run the program."""

    print('Simple Computer {0}\n'.format(version.VERSION))
    print('Program 2. Countdown')
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


if __name__ == '__main__':
    main()
