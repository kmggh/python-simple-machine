# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""Decode and execute opcodes and addresses.

Each instruction is a single value op code and a single value which
can be interpreted as an address, an extended opcode, or a set of
flags.
"""


class Decoder(object):
    """Decode op codes into instructions."""

    def __init__(self, reg, mem, alu):
        """Create the op code instruction map."""

        self.instr = Instructions(reg, mem, alu)

        self.mem = mem
        self.reg = reg

        self.op_codes = {}
        self.op_codes[0x01] = self.instr.halt
        self.op_codes[0x20] = self.instr.add
        self.op_codes[0x21] = self.instr.lda
        self.op_codes[0x22] = self.instr.sta
        self.op_codes[0x23] = self.instr.jmp
        self.op_codes[0x24] = self.instr.sza
        self.op_codes[0x25] = self.instr.sub

    def fetch_execute(self):
        """The fetch execute cycle.

        Fetch the next instruction and the value of the address following
        it.  That value, typically an address itself, is passed to the
        instruction that is executed.

        The instruction pointer is incremented by two, again typically, to
        the next address after these two.
        """

        op_code = self.mem.read(self.reg.ip)
        self.reg.ip_inc()
        addr = self.mem.read(self.reg.ip)
        self.reg.ip_inc()

        # Execute the instruction on addr.
        self.op_codes[op_code.num](addr)


class Instructions(object):
    """The instruction decoder."""

    def __init__(self, reg, mem, alu):
        """Save the registers object."""

        self.reg = reg
        self.mem = mem
        self.alu = alu

    def add(self, addr):
        """Add number from addr to accumulator."""

        val = self.mem.read(addr)
        result = self.alu.add(self.reg.accum, val)
        self.reg.accum = result

    def halt(self, addr):
        """Stop execution.

        The address is ignored and can be zero.
        """

        self.reg.run_flag = False

    def lda(self, addr):
        """Load a value from address into the accumulator."""

        val = self.mem.read(addr)
        self.reg.accum = val

    def sta(self, addr):
        """Store the value in theh accumulator to the address."""

        self.mem.write(addr, self.reg.accum)

    def jmp(self, addr):
        """Jump to addr by setting the IP to it."""

        self.reg.ip = addr

    def sza(self, addr):
        """Skip the next instruction on accumulator (flag) zero.

        If the accumulator zero_flag is True then the IP is
        incremented by two to execute the *next* instruction.

        The addr is ignored and can be zero.
        """

        if self.alu.zero_flag:
            self.reg.ip_inc()
            self.reg.ip_inc()

    def sub(self, addr):
        """Subtract number from addr to accumulator."""

        val = self.mem.read(addr)
        result = self.alu.neg_add(self.reg.accum, val)
        self.reg.accum = result
