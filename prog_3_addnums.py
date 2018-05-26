#!/usr/bin/env python3
# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""The third program that sums a series of numbers.

A sequence of numbers will be stored in memory with a starting address
as the top of the sequence (largest address).  The index register will
have the count of numbers in it.  The index register will be decremented
until it reaches zero, which is the stopping condition for adding.

Each memory address at base + index will be added into the sum.

The accumulator will be initialized to zero.

The final sum will be stored in a memory address.

We'll add  eight numbers.

    BASE = 0x10   ;; Where the numbers "start" (bottom of the addr range)
    COUNT = 0x19  ;; Address of how many numbers.
    ZERO = 0x1a   ;; A zero to store.
    RESULT = 0x18  ;; The final sum of the numbers.

    LOOP = addr 0x24  ;; label address to loop back to.

The program

     LDA ZERO    ;; Put zero in A.
     LDX COUNT   ;; Get the count from addr COUNT and put in index IDX.

LOOP DCX         ;; Decrement IDX.
     ADD,X BASE  ;; Add the number ad BASE + IDX.
     SZX         ;; Skip if IDX is now zero (last number).
     JMP LOOP    ;; else go back to LOOP.
     STA RESULT  ;; Done so store the result from A to RESULT addr.
     HLT         ;; Stop.
"""

import sys
import machine

TITLE = 'Program 3. Add Numbers'

DATA = (
    (0x10, 0x3b),  # BASE addr with number:  59
    (0x11, 0x36),  # 54
    (0x12, 0x06),  # 6
    (0x13, 0x08),  # 8
    (0x14, 0x15),  # 21
    (0x15, 0x18),  # 24
    (0x16, 0x30),  # 48
    (0x17, 0x20),  # 32
    (0x18, 0x00),  # RESULT The answer which should be 0xfc = 252.

    (0x19, 0x08),  # COUNT How many numbers to add (8)
    (0x1a, 0x00))  # ZERO for the accumulator

PROGRAM = (
    (0x20, 0x21),  # i: LDA
    (0x21, 0x1a),  # a: 0x00
    (0x22, 0x26),  # i: LDX
    (0x23, 0x19),  # a: COUNT = 0x19:  0x08
    (0x24, 0x29),  # i: DCX
    (0x25, 0x00),  # a: (ignored)
    (0x26, 0x40),  # i: ADD,X
    (0x27, 0x10),  # a: BASE
    (0x28, 0x28),  # i: SZX
    (0x29, 0x00),  # a: (ignored)
    (0x2a, 0x23),  # i: JMP
    (0x2b, 0x24),  # a: LOOP = 0x24
    (0x2c, 0x22),  # i: STA
    (0x2d, 0x18),  # a: RESULT
    (0x2e, 0x01),  # i: HLT
    (0x2f, 0x00))  # a: (ignored)


def main():
    """Run the program."""

    computer = machine.Computer(data=DATA, program=PROGRAM)
    machine.cpu.CLOCK_CYCLE_SEC = 0.10  # Overclock to 10 Hz. CAUTION!

    opt_run = len(sys.argv) >= 2 and '--run' in sys.argv
    computer.run(title=TITLE, run_flag=opt_run, print_after=True)


if __name__ == '__main__':
    main()
