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
import machine

TITLE = 'Program 2. Countdown'

DATA = (
    (0x10, -0x01),  # -1      ; To decrement the count.
    (0x11, 0x0a))  # 10      ; The initial count.

PROGRAM = (
    (0x20, 0x21),  # LDA
    (0x21, 0x11),  # 0x11
    (0x22, 0x20),  # ADD     ; Decrement with...
    (0x23, 0x10),  # 0x10    ; -1
    (0x24, 0x24),  # SZA     ; Skip if zero.
    (0x25, 0x00),  # (unused)
    (0x26, 0x23),  # JMP     ; Jump back to...
    (0x27, 0x22),  # 0x22    ; loop start.
    (0x28, 0x01),  # HLT     ; Skip to here when done.
    (0x29, 0x00))  # (unused)


def main():
    """Run the program."""

    computer = machine.Computer(data=DATA, program=PROGRAM)
    machine.cpu.CLOCK_CYCLE_SEC = 0.10  # Overclock to 10 Hz. CAUTION!

    opt_run = len(sys.argv) >= 2 and '--run' in sys.argv
    computer.run(title=TITLE, run_flag=opt_run)


if __name__ == '__main__':
    main()
