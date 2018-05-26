#!/usr/bin/env python3
# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""Test the instruction decoder."""

import unittest
import cpu
import decoder
import memory

ADDR1 = memory.Address(0x10)
ADDR2 = memory.Address(0x20)

INDEX = memory.Value(0x05)
ADDR_IDX_1 = memory.Address(0x15)
ADDR_IDX_2 = memory.Address(0x25)

ZERO = memory.Value(0)
ONE = memory.Value(1)
VAL1 = memory.Value(2)
VAL2 = memory.Value(3)


class TestInstructions(unittest.TestCase):
    def setUp(self):
        self.reg = cpu.Registers()
        self.mem = memory.Memory()
        self.alu = cpu.ArithmeticLogicUnit()
        self.mem_if = decoder.MemoryInterface(self.mem)

        self.instr = decoder.Instructions(reg=self.reg, mem=self.mem,
                                          alu=self.alu)

        self.mem.write(ADDR1, VAL1)

    def test_create(self):
        self.assertTrue(self.instr is not None)

    def test_add(self):
        self.reg.accum = VAL2
        self.instr.add(ADDR1)

        self.assertEqual(self.reg.accum, memory.Value(5))

        self.reg.run_flag = True
        self.instr.halt(ADDR1)

        self.assertFalse(self.reg.run_flag)

    def test_lda(self):
        self.instr.lda(ADDR1)

        self.assertEqual(self.reg.accum, VAL1)

    def test_sta(self):
        self.reg.accum = VAL2
        self.instr.sta(ADDR1)

        value = self.mem.read(ADDR1)
        self.assertEqual(value, VAL2)

    def test_jmp(self):
        self.reg.ip = ADDR1
        self.instr.jmp(ADDR2)

        self.assertEqual(self.reg.ip, ADDR2)

    def test_sza_not_zero(self):
        self.reg.ip = ADDR1
        self.alu.zero_flag = False
        self.instr.sza(memory.Address(0x00))

        self.assertEqual(self.reg.ip, ADDR1)

    def test_sza_zero(self):
        self.reg.ip = ADDR1
        self.alu.zero_flag = True
        self.instr.sza(memory.Address(0x00))

        addr2 = memory.Address(ADDR1.num + 2)
        self.assertEqual(self.reg.ip, addr2)

    def test_sub(self):
        self.reg.accum = VAL2
        self.instr.sub(ADDR1)

        self.assertEqual(self.reg.accum, memory.Value(1))

    def test_ldx(self):
        self.instr.ldx(ADDR1)

        self.assertEqual(self.reg.idx, VAL1)

    def test_stx(self):
        self.reg.idx = VAL2
        self.instr.stx(ADDR1)

        value = self.mem.read(ADDR1)
        self.assertEqual(value, VAL2)

    def test_dcx(self):
        self.reg.idx = VAL2
        self.instr.dcx(ZERO)  # Ignored addr.

        dec_val = VAL2.inc(-1)
        self.assertEqual(self.reg.idx, dec_val)
        self.assertFalse(self.reg.zerox_flag)

    def test_dcx_zero(self):
        self.reg.idx = ONE
        self.instr.dcx(ZERO)  # Ignored addr.

        self.assertEqual(self.reg.idx, ZERO)
        self.assertTrue(self.reg.zerox_flag)

    def test_szx_not_zero(self):
        self.reg.ip = ADDR1
        self.reg.zerox_flag = False
        self.instr.szx(ZERO)

        self.assertEqual(self.reg.ip, ADDR1)

    def test_szx_zero(self):
        self.reg.ip = ADDR1
        self.reg.zerox_flag = True
        self.instr.szx(ZERO)

        addr2 = memory.Address(ADDR1.num + 2)
        self.assertEqual(self.reg.ip, addr2)

    def test_addx(self):
        self.reg.accum = VAL2
        self.reg.idx = INDEX
        self.mem_if.write(ADDR1, VAL1, index=INDEX)

        self.instr.addx(ADDR1)

        self.assertEqual(self.reg.accum, memory.Value(5))

    def test_ldax(self):
        self.reg.idx = INDEX
        self.mem_if.write(ADDR1, VAL1, index=INDEX)

        self.instr.ldax(ADDR1)

        self.assertEqual(self.reg.accum, VAL1)

    def test_stax(self):
        self.reg.idx = INDEX
        self.reg.accum = VAL2

        self.instr.stax(ADDR1)

        value = self.mem_if.read(ADDR1, index=INDEX)

        self.assertEqual(value, VAL2)


class FakeInstruction(object):
    """A fake instruction for decoder testing."""

    def __init__(self):
        """Initialize addr."""

        self.addr = None

    def instr(self, addr):
        """The fake instruction.

        We save the addr so the call can be verified.
        """

        self.addr = addr


class TestDecoder(unittest.TestCase):
    def setUp(self):
        self.reg = cpu.Registers()
        self.mem = memory.Memory()
        self.alu = cpu.ArithmeticLogicUnit()

        self.decoder = decoder.Decoder(self.reg, self.mem, self.alu)

    def test_create(self):
        self.assertTrue(self.decoder is not None)

    def test_opcodes(self):
        self.assertEqual(self.decoder.op_codes[0x01], self.decoder.instr.halt)

    def test_fetch_execute(self):
        fake_obj = FakeInstruction()
        self.decoder.op_codes[0x01] = fake_obj.instr

        # The op code.
        self.mem.write(memory.Address(0x10), memory.Value(0x01))

        # The addr argument.
        self.mem.write(memory.Address(0x11), memory.Value(0x22))

        self.reg.ip = memory.Address(0x10)

        self.decoder.fetch_execute()

        self.assertEqual(self.reg.ip, memory.Address(0x12))
        self.assertEqual(fake_obj.addr, memory.Address(0x22))


class TestMemoryInterface(unittest.TestCase):
    def setUp(self):
        self.mem_obj = memory.Memory()
        self.mem_if = decoder.MemoryInterface(self.mem_obj)

    def test_create(self):
        self.assertTrue(self.mem_if is not None)

    def test_read_zero_value(self):
        addr = memory.Address(0x20)
        value = memory.Value(0)
        self.assertEqual(self.mem_if.read(addr), value)

    def test_write_value(self):
        value = memory.Value(0x0a)
        addr = memory.Address(0x20)
        self.mem_if.write(addr, value)
        self.assertEqual(self.mem_if.read(addr), value)

    def test_read_index(self):
        value = memory.Value(0x0a)
        addr = memory.Address(0x10)
        addr_idx = memory.Address(0x20)
        index_val = memory.Value(0x10)
        self.mem_if.write(addr_idx, value)

        read_value = self.mem_if.read(addr, index=index_val)

        self.assertEqual(read_value, value)

    def test_write_index(self):
        value = memory.Value(0x0a)
        addr = memory.Address(0x10)
        index_val = memory.Value(0x10)

        self.mem_if.write(addr, value, index=index_val)
        read_value = self.mem_if.read(addr, index=index_val)

        self.assertEqual(read_value, value)
