# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""Decode and execute opcodes and addresses.

Each instruction is a single value op code and a single value which
can be interpreted as an address, an extended opcode, or a set of
flags.
"""

import error


class IndexCarryError(error.Error):
    """When indexing an address the carry was true which is an overflow."""


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
        self.op_codes[0x26] = self.instr.ldx
        self.op_codes[0x27] = self.instr.stx
        self.op_codes[0x28] = self.instr.szx
        self.op_codes[0x29] = self.instr.dcx
        self.op_codes[0x40] = self.instr.addx  # ADD,X
        self.op_codes[0x41] = self.instr.ldax  # LDA,X
        self.op_codes[0x42] = self.instr.stax  # STA,X

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


class MemoryInterface(object):
    """A memory interface that handles indexing."""

    def __init__(self, mem_obj):
        """Attach memory."""

        self.mem = mem_obj

    def index_addr(self, addr, index):
        """Apply an index to an address and return the new address."""

        if index is not None:
            addr, carry = addr + index

            if carry:
                msg = 'Overflow with addr {0} and index {1}'
                raise IndexCarryError(msg.format(addr, index))

        return addr

    def write(self, addr, value, index=None):
        """Write a value into memory at this address plus index."""

        addr_idx = self.index_addr(addr, index)
        self.mem.write(addr_idx, value)

    def read(self, addr, index=None):
        """Return the value at the given address plus index."""

        addr_idx = self.index_addr(addr, index)
        value = self.mem.read(addr_idx)

        return value


class Instructions(object):
    """The instruction decoder."""

    def __init__(self, reg, mem, alu):
        """Save the registers object."""

        self.reg = reg
        self.mem = mem
        self.alu = alu

        self.mem_if = MemoryInterface(self.mem)

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
        """Store the value in the accumulator to the address."""

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

    def ldx(self, addr):
        """Load a value from address into the index."""

        val = self.mem.read(addr)
        self.reg.idx = val

    def stx(self, addr):
        """Store the value in the index to the address."""

        self.mem.write(addr, self.reg.idx)

    def dcx(self, addr):
        """Decement the index register by one.

        Note that the addr is ignored.
        """

        self.reg.idx = self.reg.idx.inc(-1)
        self.reg.zerox_flag = self.reg.idx.eq_zero()

    def szx(self, addr):
        """Skip the next instruction on zerox (flag) zero.

        If the register zerox_flag is True then the IP is
        incremented by two to execute the *next* instruction.

        The addr is ignored and can be zero.
        """

        if self.reg.zerox_flag:
            self.reg.ip_inc()
            self.reg.ip_inc()

    def addx(self, addr):
        """Add number from addr plus index to accumulator."""

        val = self.mem_if.read(addr, index=self.reg.idx)
        result = self.alu.add(self.reg.accum, val)
        self.reg.accum = result

    def ldax(self, addr):
        """Add number from addr plus index to accumulator."""

        val = self.mem_if.read(addr, index=self.reg.idx)
        self.reg.accum = val

    def stax(self, addr):
        """Add number from addr plus index to accumulator."""

        self.mem_if.write(addr, self.reg.accum, index=self.reg.idx)
