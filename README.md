# Simple Machine

Ken Guyton<br />
Mon 2018-05-07 19:14:05 -0400

A simple computer emulated in Python.

This is a ship in a bottle.  It's a little, simple computer emulator
written over a few days to illustrate some of the basic ideas in the
design of a computer.  Most of the simple concepts illustrated here
are still applicable to computer design today, but with many
embellishments and much added technology.  The purpose of building
this simulator was for the joy of doing it and perhaps as a way to
show someone how a computer works.

The ideas here were inspired to some extent by the PDP-8, the 6502,
maybe Knuth's MIX computer though I'm not sure about that now, the
MIT SICP class from 1986 and other sources I've no doubt forgotten.

## To run

There are two programs currently included here.  The first is
prog_1a_add.py which is a simple addition of 5 = 2 + 3.  It illustrates
a very simple program.

From the command line you can run it this way.

    python3 prog_1a_add.py --run

The second program, prog_2a_countdown.py, counts down from 10 to zero.

    python3 prog_2a_countdown.py --run

As you can see, you need Python 3 installed to run these programs.
It's free and easily found on-line along with plenty of instructions on
how to install it.

## The computer

This is a true eight bit computer.  Addresses and data values are all
eight bits meaning you can't have a number larger than 255 and you can
only store 256 instructions in memory.  It would be easy to extend
this model to 16-bit addresses and even 16-bit values.

It is possible to have negative values represented by a negative flag
in a value, so you can make a technical argument that these are
actually nine bit data values.  Negation is handled internally so
there's no implementation of anything like one's or two's complement
binary values.  In fact, all numbers are Python numbers and data and
addresses are Python objects in the code.

There are only two registers in the computer, the accumulator and the
instruction pointer, again both are eight bits.

There are several flags, the run flag, the overflow flag and the zero
flag.  The run flag has to be set for a program to run.  The overflow
flag should be set if a value overflows during an arithmetic
operation.  The zero flag is set when an arithmetic operation results
in a zero in the accumulator.

The machine language currently consists of seven instructions but more
will certainly be added.  The instructions and there op codes are as
follows.

        0x01 halt - Stop the computer.
        0x20 add  - Add a number from the address to the accumulator.
        0x21 lda  - Load a number from the address to the accumulator.
        0x22 sta  - Store a number from the accumulator to the address.
        0x23 jmp  - Set the instruction pointer to the given address.
        0x24 sza  - Skip the next two values (instruction) on zero.
        0x25 sub  - Subtract a number from the address from the accumulator.

Note that we represent the op codes here as hexadecimal numbers but
any number form or base can be used.

Each instruction is two bytes, i.e., two values.  The first is the op code
and the second is an address.  Instructions like halt and sza which
don't use the address so it's ignored.

## The implementation

There are several modules and classes used in the Python
representation.

    cpu
        Registers
        Clock
        ArithmeticLogicUnit
    memory
        Address
        Value
        Memory
    decoder
        Instructions
        Decoder
    machine
        Computer

The modules and classes are described in the documentation in the
code.

## Copyright

All the files, documentation and program code here is copyright 2018
by Ken Guyton.  All rights reserved.  Licenses for use are available
by request.
