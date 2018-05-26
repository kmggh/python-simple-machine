#!/usr/bin/env python3
# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""Test the CPU."""

import unittest
import cpu
import decoder
import memory

VALUE_0A_HEX = 0x0a
ADDR_20_HEX = 0x20
SIZE = 255

ZERO_ADDR = memory.Address(0)
ZERO_VAL = memory.Value(0)


class TestRegisters(unittest.TestCase):
    def setUp(self):
        self.reg = cpu.Registers()

    def test_create(self):
        self.assertTrue(self.reg is not None)

    def test_values(self):
        self.assertEqual(self.reg.accum, ZERO_VAL)
        self.assertEqual(self.reg.idx, ZERO_VAL)
        self.assertEqual(self.reg.ip, ZERO_ADDR)

        self.assertFalse(self.reg.run_flag)
        self.assertFalse(self.reg.zerox_flag)

    def test_ip_inc(self):
        self.assertEqual(self.reg.ip, ZERO_ADDR)
        self.reg.ip_inc()
        self.assertEqual(self.reg.ip, ZERO_ADDR.inc())


class TestArithmeticLogicUnit(unittest.TestCase):
    def setUp(self):
        self.alu = cpu.ArithmeticLogicUnit()

    def test_create(self):
        self.assertTrue(self.alu is not None)

    def test_add(self):
        val1 = memory.Value(2)
        val2 = memory.Value(3)

        self.assertEqual(self.alu.add(val1, val2), memory.Value(5))
        self.assertFalse(self.alu.overflow_flag)
        self.assertFalse(self.alu.zero_flag)

    def test_overflow(self):
        val1 = memory.Value(255)
        val2 = memory.Value(3)

        self.assertEqual(self.alu.add(val1, val2), memory.Value(2))
        self.assertTrue(self.alu.overflow_flag)
        self.assertFalse(self.alu.zero_flag)

    def test_zero(self):
        val1 = memory.Value(255)
        val2 = memory.Value(1)

        self.assertEqual(self.alu.add(val1, val2), memory.Value(0))
        self.assertTrue(self.alu.overflow_flag)
        self.assertTrue(self.alu.zero_flag)

    def test_neg_add(self):
        val1 = memory.Value(5)
        val2 = memory.Value(3)

        result = self.alu.neg_add(val1, val2)

        self.assertEqual(result, memory.Value(2))
        self.assertFalse(self.alu.overflow_flag)
        self.assertFalse(self.alu.zero_flag)

    def test_add_neg(self):
        val1 = memory.Value(5)
        val2 = memory.Value(-3)

        result = self.alu.add(val1, val2)

        self.assertEqual(result, memory.Value(2))
        self.assertFalse(self.alu.overflow_flag)
        self.assertFalse(self.alu.zero_flag)


class TestClock(unittest.TestCase):
    def setUp(self):
        self.reg = cpu.Registers()
        self.mem = memory.Memory()
        self.alu = cpu.ArithmeticLogicUnit()
        self.decoder = decoder.Decoder(self.reg, self.mem, self.alu)

        self.clock = cpu.Clock(self.reg, self.decoder)

    def test_create(self):
        self.assertTrue(self.reg is not None)
