#!/usr/bin/env python

from __future__ import print_function

# Read button input through a CD4021 shift register

# Thanks to WiringPi,
# https://github.com/WiringPi/WiringPi/blob/9a8f8bee5df60061645918231110a7c2e4d3fa6b/devLib/piNes.c

import RPi.GPIO as GPIO
import time

class CD4021:
    pulse_time = .000025     # gordonDrogon says 25 microseconds, .000025

    def __init__(self, clock, latch, data):
        self.latch = latch
        self.clock = clock
        self.data = data

        # Use GPIO numbering:
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.latch, GPIO.OUT)
        GPIO.setup(self.clock, GPIO.OUT)
        GPIO.setup(self.data, GPIO.IN)

    def pulse_pin(self, pin):
        '''Pulse a pin high, then low'''
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(CD4021.pulse_time)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(CD4021.pulse_time)

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
    # Python has no native way to print binary unsigned numbers. Lame!
    def tobin(data, width=8):
        data_str = bin(data & (2**width-1))[2:].zfill(width)
        return data_str

    shiftr = CD4021(11, 9, 4)
    try:
        while True:
            # b1 = shiftr.read_one_byte()
            # print(format(b1, '#010b'))
            bytes = shiftr.read_n_bytes(3)
            print('   '.join([tobin(b, 8) for b in bytes]))
            print('   '.join(["%8x" % b for b in bytes]))
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()


