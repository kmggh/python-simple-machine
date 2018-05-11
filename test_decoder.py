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
VAL1 = memory.Value(2)
VAL2 = memory.Value(3)


class TestInstructions(unittest.TestCase):
    def setUp(self):
        self.reg = cpu.Registers()
        self.mem = memory.Memory()
        self.alu = cpu.ArithmeticLogicUnit()

        self.instr = decoder.Instructions(reg=self.reg, mem=self.mem,
                                          alu=self.alu)

        self.mem.write(ADDR1, VAL1)

    def test_create(self):
        self.assertTrue(self.instr is not None)

    def test_add(self):
        self.reg.accum = VAL2
        self.instr.add(ADDR1)

        self.assertEqual(self.reg.accum, memory.Value(5))

    def test_halt(self):
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
