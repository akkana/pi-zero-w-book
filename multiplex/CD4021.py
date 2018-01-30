#!/usr/bin/env python

from __future__ import print_function

# Read button input through a CD4021 shift register

# Thanks to WiringPi,
# https://github.com/WiringPi/WiringPi/blob/9a8f8bee5df60061645918231110a7c2e4d3fa6b/devLib/piNes.c

import RPi.GPIO as GPIO
import time

class CD4021:
    pulse_time = .000025     # gordonDrogon says 25 microseconds, .000025

    def __init__(self, clock, latch, data, num_chips=1):
        self.latch = latch   # aka M on the pinout, pin 9
        self.clock = clock   # aka CLK, pin 10
        self.data = data     # data out, pin 3, labeled as Q7 or Q8
        # pinout diagrams seem to vary on how they number the Q pins:
        # the pins all send out the same data but the early Qs are one
        # and two clock pulses behind the biggest Q, which should be
        # on pin 3. So use that one.

        self.num_chips = num_chips

        GPIO.setup(self.latch, GPIO.OUT)
        GPIO.setup(self.clock, GPIO.OUT)
        GPIO.setup(self.data, GPIO.IN)

    def pulse_pin(self, pin):
        '''Pulse a pin high, then low'''
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(CD4021.pulse_time)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(CD4021.pulse_time)

    def read_shift_regs(self):
        '''Read the results of the shift registers.
           Returns a list of bytes, one for each chip.
        '''
        bytelist = []

        # Toggle Latch - which presents the first bit
        self.pulse_pin(self.latch)

        for i in range(self.num_chips):
            value = GPIO.input(self.data)
            # Now get the rest of the bits with the clock
            for i in range(7):
                self.pulse_pin(self.clock)
                value = (value << 1) | GPIO.input(self.data)

            bytelist.append(value)
            self.pulse_pin(self.clock)
            # XXX This means one extra clock pulse at the end of
            # all the reading, but I think that'll be okay.

        return bytelist

    # XXX Should remove read_*byte* after verifying that read_shift_regs
    # works okay for keyboard.py.
    def read_byte(self):
        # Read first bit
        value = GPIO.input(self.data)

        # Now get the rest of the bits with the clock
        for i in range(7):
            self.pulse_pin(self.clock)
            value = (value << 1) | GPIO.input(self.data)

        return value

    def read_one_byte(self):
        # Toggle Latch - which presents the first bit
        self.pulse_pin(self.latch)

        return self.read_byte()

    def read_n_bytes(self, numbytes):
        bytesread = [ self.read_one_byte() ]

        for i in range(1, numbytes):
            # For subsequent bytes, we don't want another latch but
            # read_byte doesn't start with a clock pulse, so do it here.
            self.pulse_pin(self.clock)
            bytesread.append(self.read_byte())

        return bytesread

if __name__ == '__main__':
    # Use GPIO numbering:
    GPIO.setmode(GPIO.BCM)

    # Python has no native way to print binary unsigned numbers. Lame!
    def tobin(data, width=8):
        data_str = bin(data & (2**width-1))[2:].zfill(width)
        return data_str

    shiftr = CD4021(clock=11, latch=9, data=4, num_chips=3)
    # For compatibility with SN74LS165 examples and SPI attempts:
    # shiftr = CD4021(clock=11, latch=7, data=9, num_chips=1)
    try:
        while True:
            # bytelist = [ shiftr.read_one_byte() ]
            # bytelist = shiftr.read_n_bytes(3)
            bytelist = shiftr.read_shift_regs()
            print('   '.join([tobin(b, 8) for b in bytelist]))
            print('   '.join(["%8x" % b for b in bytelist]))
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()


