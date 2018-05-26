# coding: utf-8
# © 2018 by Ken Guyton.  All rights reserved.

"""The central processing unit.

This computer runs in slow motion with a clock cycle time of one second.

The speed is 1 Hz.
"""

import time
import memory

CLOCK_CYCLE_SEC = 1


class Registers(object):
    """The collection of registers in the CPU."""

    def __init__(self):
        """Initialize the registers."""

        self.accum = memory.Value(0)
        self.ip = memory.Address(0)
        self.idx = memory.Address(0)

        self.run_flag = False
        self.zerox_flag = False

    def ip_inc(self):
        """Increment the IP."""

        self.ip = self.ip.inc()


class Clock(object):
    """The clock that drives the system."""

    def __init__(self, reg, decoder):
        """Save the registers and decoder."""

        self.reg = reg
        self.decoder = decoder

    def run(self):
        """Start the clock and computer running.

        The computer runs the fetch execute cycle until the
        run_flag is false.  Then this method exits.  The memory
        and particularly the instruction pointer should be
        initialized before starting.
        """

        self.reg.run_flag = True

        while self.reg.run_flag:
            msg = 'blink... IP: {0} A: {1} IDX: {2}'
            print(msg.format(self.reg.ip.hex(), self.reg.accum.hex(),
                             self.reg.idx.hex()))

            self.decoder.fetch_execute()
            time.sleep(CLOCK_CYCLE_SEC)


class ArithmeticLogicUnit(object):
    """The ALU that does arithmetic."""

    def __init__(self):
        """Initialize the ALU."""

        self.overflow_flag = False
        self.zero_flag = False

    def add(self, val1, val2):
        """Add two values and return the resulting sum value."""

        val1_num = val1.get_num()
        val2_num = val2.get_num()

        total_num = val1_num + val2_num

        if total_num > 255:
            self.overflow_flag = True
            total_num = total_num % 256
        else:
            self.overflow_flag = False

        self.zero_flag = (total_num == 0)

        return memory.Value(total_num)

    def neg_add(self, val1, val2):
        """First negate val2 then add."""

        neg_val2 = val2.copy()
        neg_val2.negate()

        return self.add(val1, neg_val2)
