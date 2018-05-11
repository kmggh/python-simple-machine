# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""Computer memory.

One-byte values in one-byte addresses.
"""

SIZE = 256


class Error(Exception):
    """Memory errors."""


class ValueRangeError(Error):
    """The value is out of range."""


class Value(object):
    """A value from memory."""

    def __init__(self, num):
        """Initialize with an input num.

        Args:
          num: int. The num must be on range(256).
        """

        if num < 0:
            self.negative_flag = True
            num = -num
        else:
            self.negative_flag = False

        if num < 0 or num > 255:
            raise ValueRangeError(num)
        else:
            self.num = num

    def hex(self):
        """Return a two digit hex representation."""

        return '0x{0:02x}'.format(self.num)

    def oct(self):
        """Return a three digit octal representation."""

        return '0o{0:03o}'.format(self.num)

    def dec(self):
        """Return a two digit decimal representation."""

        return '{0:03d}'.format(self.num)

    def __eq__(self, a_value):
        """Compare two values for equality."""

        eq_num = self.num == a_value.num
        eq_neg = self.negative_flag == a_value.negative_flag

        return eq_num and eq_neg

    def __ne__(self, a_value):
        """Compare two values for inequality."""

        ne_num = self.num != a_value.num
        ne_neg = self.negative_flag != a_value.negative_flag

        return ne_num or ne_neg

    def copy(self):
        """Create a copy of this value."""

        copy_value = self.__class__(self.num)
        copy_value.negative_flag = self.negative_flag

        return copy_value

    def inc(self, increment=1):
        """Increment by some value."""

        new_value = self.__class__(self.num + increment)

        return new_value

    def negate(self):
        """Negate a value."""

        self.negative_flag = not self.negative_flag

    def get_num(self):
        """Get the arithmetic number value.

        This means if the negative flag is set, a negative number is
        returned.
        """

        if self.negative_flag:
            num = -self.num
        else:
            num = self.num

        return num

    def __repr__(self):
        """A str representation of the value."""

        return 'Value({0}, neg={1})'.format(self.hex(), self.negative_flag)


class Address(Value):
    """A memory address which is also on the range(256)."""

    def __repr__(self):
        """A str representation of the value."""

        return 'Address({0})'.format(self.hex())


class Memory(object):
    """Computer memory with a given number of addresses."""

    def __init__(self, size=SIZE):
        """Create a list of values for the size.

        If a location is None, it's a Value(0).
        """

        self.mem_list = [None] * size
        self.size = size

    def read(self, addr):
        """Return the value at the given address."""

        value = self.mem_list[addr.num]
        if value is None:
            value = Value(0)

        return value

    def write(self, addr, value):
        """Write a value into memory at this address."""

        value_copy = value.copy()
        self.mem_list[addr.num] = value_copy

    def display(self, addr):
        """Display a single address."""

        value = self.read(addr)
        addr_value = '{0} {1}'.format(addr.hex(), value.hex())

        return addr_value

    def display_range(self, addr_start, addr_end):
        """Display a range of addresses and values."""

        addr = addr_start
        display_list = []
        while addr != addr_end:
            display_list.append(self.display(addr))
            addr = addr.inc()

        return '\n'.join(display_list)
