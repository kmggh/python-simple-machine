#!/usr/bin/env python3
# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""Test the memory."""

import unittest
import memory

VALUE_0A_HEX = 0x0a
VALUE_10_HEX = 0x10
ADDR_20_HEX = 0x20
SIZE = 256


class TestValue(unittest.TestCase):
    def setUp(self):
        self.value = memory.Value(VALUE_0A_HEX)

    def test_create(self):
        self.assertTrue(self.value is not None)
        self.assertFalse(self.value.negative_flag)

    def test_hex(self):
        self.assertEqual(self.value.hex(), '0x0a')

    def test_oct(self):
        self.assertEqual(self.value.oct(), '0o012')

    def test_dec(self):
        self.assertEqual(self.value.dec(), '010')

    def test_copy(self):
        copy_value = self.value.copy()
        self.assertEqual(copy_value, self.value)

    def test_copy_neg(self):
        neg_value = memory.Value(-VALUE_0A_HEX)
        neg_copy_value = neg_value.copy()
        self.assertEqual(neg_copy_value, neg_value)

    def test_negative(self):
        value = memory.Value(-VALUE_0A_HEX)
        self.assertEqual(value.hex(), '0x0a')
        self.assertTrue(value.negative_flag)

    def test_get_num_pos(self):
        num = self.value.get_num()
        self.assertEqual(num, VALUE_0A_HEX)

    def test_get_num_neg(self):
        value = memory.Value(VALUE_0A_HEX)
        value.negate()
        num = value.get_num()
        self.assertEqual(num, -VALUE_0A_HEX)

    def test_eq_zero_not(self):
        value = memory.Value(VALUE_0A_HEX)

        self.assertFalse(value.eq_zero())

    def test_eq_zero(self):
        value = memory.Value(0)

        self.assertTrue(value.eq_zero())

    def test_add(self):
        result, carry = memory.Value(VALUE_0A_HEX) + memory.Value(VALUE_10_HEX)

        self.assertEqual(result, memory.Value(0x1a))
        self.assertFalse(carry)

    def test_add_neg(self):
        val1 = memory.Value(VALUE_10_HEX)
        val2 = memory.Value(- VALUE_0A_HEX)
        result, carry = val1 + val2

        self.assertEqual(result, memory.Value(0x06))
        self.assertFalse(carry)

    def test_add_over(self):
        val1 = memory.Value(0xf0)
        val2 = memory.Value(0xf0)

        result, carry = val1 + val2

        self.assertEqual(result, memory.Value(0xe0))
        self.assertTrue(carry)

    def test_add_neg_result(self):
        val1 = memory.Value(- VALUE_10_HEX)
        val2 = memory.Value(VALUE_0A_HEX)
        result, carry = val1 + val2

        self.assertEqual(result, memory.Value(-0x06))
        self.assertFalse(carry)

    def test_is_printable(self):
        self.assertFalse(memory.Value(0x01).is_printable())
        self.assertTrue(memory.Value(0x21).is_printable())
        self.assertTrue(memory.Value(0x50).is_printable())
        self.assertTrue(memory.Value(0x65).is_printable())
        self.assertFalse(memory.Value(0x7f).is_printable())
        self.assertFalse(memory.Value(0xa0).is_printable())


class TestAddress(unittest.TestCase):
    def setUp(self):
        self.addr = memory.Address(VALUE_0A_HEX)

    def test_create(self):
        self.assertTrue(self.addr is not None)

    def test_hex(self):
        self.assertEqual(self.addr.hex(), '0x0a')

    def test_oct(self):
        self.assertEqual(self.addr.oct(), '0o012')

    def test_dec(self):
        self.assertEqual(self.addr.dec(), '010')

    def test_copy(self):
        copy_addr = self.addr.copy()
        self.assertEqual(copy_addr, self.addr)

    def test_inc(self):
        self.assertEqual(self.addr.inc(), memory.Address(VALUE_0A_HEX + 1))


class TestMemory(unittest.TestCase):
    def setUp(self):
        self.mem = memory.Memory(SIZE)

    def test_create(self):
        self.assertTrue(self.mem is not None)

    def test_read_zero_value(self):
        addr = memory.Address(ADDR_20_HEX)
        value = memory.Value(0)
        self.assertEqual(self.mem.read(addr), value)

    def test_write_value(self):
        value = memory.Value(VALUE_0A_HEX)
        addr = memory.Address(ADDR_20_HEX)
        self.mem.write(addr, value)
        self.assertEqual(self.mem.read(addr), value)

    def test_display_addr(self):
        value = memory.Value(VALUE_0A_HEX)
        addr = memory.Address(ADDR_20_HEX)
        self.mem.write(addr, value)

        self.assertEqual(self.mem.display(addr), '0x20 0x0a')

    def test_display_addr_not_printable(self):
        value = memory.Value(VALUE_0A_HEX)
        addr = memory.Address(ADDR_20_HEX)
        self.mem.write(addr, value)

        self.assertEqual(self.mem.display_printable(addr), '0x20 0x0a   ')

    def test_display_addr_printable(self):
        value = memory.Value(0x43)
        addr = memory.Address(ADDR_20_HEX)
        self.mem.write(addr, value)

        self.assertEqual(self.mem.display_printable(addr), '0x20 0x43  C')

    def test_display_range(self):
        value = memory.Value(VALUE_0A_HEX)
        addr1 = memory.Address(ADDR_20_HEX - 1)
        addr2 = memory.Address(ADDR_20_HEX + 2)
        addr = memory.Address(ADDR_20_HEX)
        self.mem.write(addr, value)

        self.assertEqual(self.mem.display_range(addr1, addr2),
                         '0x1f 0x00\n0x20 0x0a\n0x21 0x00')

    def test_read_neg(self):
        value = memory.Value(-VALUE_0A_HEX)
        addr = memory.Address(ADDR_20_HEX)
        self.mem.write(addr, value)

        value_expected = memory.Value(-VALUE_0A_HEX)
        self.assertEqual(self.mem.read(addr), value_expected)
