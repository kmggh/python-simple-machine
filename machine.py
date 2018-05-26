# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""The simple machine."""

import cpu
import decoder
import memory
import version

ADDR = memory.Address
VALUE = memory.Value

START_PROG = ADDR(0x20)


class Computer(object):
    """The assembled computer."""

    def __init__(self, data=None, program=None, start_ip=START_PROG):
        """Initialize and assemble the parts.

        Args:
            data: list of tuple pairs.  The pairs are numbers, address and
                value.
            program: list of tuple pairs.  The pairs are numbers, address and
                value.
            start_ip: int.  This is an int, typically in hex, the starting
                address of the program code.
        """

        if data is None:
            data = ()
        self.data = data

        if program is None:
            program = ()
        self.program = program

        self.setup_computer(start_ip)

    def setup_computer(self, start_ip):
        """Build the computer."""

        self.reg = cpu.Registers()
        self.mem = memory.Memory()
        self.alu = cpu.ArithmeticLogicUnit()
        self.decoder_obj = decoder.Decoder(self.reg, self.mem, self.alu)
        self.clock = cpu.Clock(self.reg, self.decoder_obj)

        self.reg.ip = start_ip

    def read_in_data(self, data_in):
        """Read in tuple pairs of address data and store."""

        data = [(ADDR(a), VALUE(v)) for a, v in data_in]

        for pair in data:
            self.mem.write(*pair)

    def store_data(self):
        """Store our data."""

        self.read_in_data(self.data)

    def store_program(self):
        """Store the program."""

        self.read_in_data(self.program)

    def prog_display(self):
        """Display the data and program memory."""

        return self.display_list(self.program)

    def data_display(self, printable=False):
        """Display the data memory."""

        return self.display_list(self.data, printable)

    def display_list(self, a_list, printable=False):
        """Display a list of address value tuple pairs."""

        start_num = a_list[0][0]
        end_num = a_list[-1][0] + 1

        start_addr = memory.Address(start_num)
        end_addr = memory.Address(end_num)

        return self.mem.display_range(start_addr, end_addr, printable)

    def run(self, title, run_flag=False, printable=False, print_after=False):
        """Run the program."""

        print('Simple Computer {0}\n'.format(version.VERSION))
        print(title)
        print()

        self.store_data()
        self.store_program()

        print('Data:\n')
        print(self.data_display(printable=printable))
        print()

        print('Program:\n')
        print(self.prog_display())
        print()

        if run_flag:
            print('*** Running...\n')

            self.clock.run()
            print()
            print('*** Halted.')
            print()

        if run_flag and print_after:
            print('Data:\n')
            print(self.data_display(printable=printable))
            print()
