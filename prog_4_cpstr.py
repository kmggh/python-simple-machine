#!/usr/bin/env python3
# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""The third program that copies a string.

This is how you might, for example, copy data from a network or disk
block buffer into a place in memory to save it.

This program copies a str from one memory location to another.  This
version will use the Pascal-like format where the length of the string
is at the beginning, the first byte.  A single value (byte) length
means the string is limited to 255 characters, which was exactly the
case with some early languages.

It would be instructive to write a different version that uses the C
approach where a terminating null 0x00 character marks the end of the
str.  Of course this can lead to security vulnerabilities and is a
major problem today, so I'm reverting to the old scheme which is
inherently safer.  We'll put our strings up in the upper memory above
the program at 0x40 and 0x60 for the source and destination, respectively.

Since idx has decrement and szx skip on zero we'll copy the string
from the back to the front.  The result is the same.

SRC = 0x40
DST = 0x50

     LDX SRC      ;; Get the count
     STX DST      ;; Store the count at the start of the other str.

LOOP LDA,X SRC    ;; Get a char
     STA,X DST    ;; Store in dest
     DCX          ;; Decrement to next char
     SZX          ;; Skip on idx zero
     JMP LOOP     ;; Jump to the LOOP addr
     HLT          ;; Else we're done
"""

import sys
import machine

TITLE = 'Program 4. Copy String'

DATA = (
    (0x40, 0x0d),  # length = 13
    (0x41, 0x48),  # H
    (0x42, 0x65),  # e
    (0x43, 0x6c),  # l
    (0x44, 0x6c),  # l
    (0x45, 0x6f),  # o
    (0x46, 0x2c),  # ,
    (0x47, 0x20),  # spc
    (0x48, 0x57),  # W
    (0x49, 0x6f),  # o
    (0x4a, 0x72),  # r
    (0x4b, 0x6c),  # l
    (0x4c, 0x64),  # d
    (0x4d, 0x21),  # !
    (0x5d, 0x00))  # End of copied str just to cause this range to display.

PROGRAM = (
    (0x20, 0x26),  # i: LDX
    (0x21, 0x40),  # a: 0x40 = SRC -->  count 13
    (0x22, 0x27),  # i: STX
    (0x23, 0x50),  # a: 0x50 = DST <-- count
    (0x24, 0x41),  # i: LDA,X    LOOP = 0x24
    (0x25, 0x40),  # a: SRC
    (0x26, 0x42),  # i: STA,X
    (0x27, 0x50),  # a: DST
    (0x28, 0x29),  # i: DCX
    (0x29, 0x00),  # a: (ignored)
    (0x2a, 0x28),  # i: SZX
    (0x2b, 0x00),  # a: (ignored)
    (0x2c, 0x23),  # i: JMP
    (0x2d, 0x24),  # a: 0x24 = LOOP
    (0x2e, 0x01),  # i: HLT
    (0x2f, 0x00))  # a: (ignored)


def main():
    """Run the program."""

    computer = machine.Computer(data=DATA, program=PROGRAM)
    machine.cpu.CLOCK_CYCLE_SEC = 0.10  # Overclock to 10 Hz. CAUTION!

    opt_run = len(sys.argv) >= 2 and '--run' in sys.argv
    computer.run(title=TITLE, run_flag=opt_run, printable=True,
                 print_after=True)


if __name__ == '__main__':
    main()
