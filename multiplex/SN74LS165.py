#!/usr/bin/env python

from __future__ import print_function

# Read button input through an SN74LS165 shift register.
# Adapted from the Arduino version at
# https://playground.arduino.cc/Code/ShiftRegSN74HC165N

import RPi.GPIO as GPIO
import time

class SN74LS165:
    pulse_time = .000005     # 5 microseconds

    def __init__(self, clock, latch, data, clock_enable, num_chips=1):
        self.latch = latch                 # AKA pload AKA PL, pin 1
        self.clock = clock                 # AKA CP, pin 2
        self.data = data                   # AKA Q7, pin 9
        self.clock_enable = clock_enable   # AKA CE, pin 15

        self.num_chips = num_chips
        self.datawidth = self.num_chips * 8

        GPIO.setup(self.latch, GPIO.OUT)
        GPIO.setup(self.clock, GPIO.OUT)
        GPIO.setup(self.data, GPIO.IN)
        GPIO.setup(self.clock_enable, GPIO.OUT)

    def read_shift_regs(self):
        # Logic copied from the Arduino program.
        # XXX Doesn't make room fo data width for higher numbers of chips.
        GPIO.output(self.clock_enable, GPIO.HIGH)
        GPIO.output(self.latch, GPIO.LOW)
        time.sleep(SN74LS165.pulse_time)
        GPIO.output(self.latch, GPIO.HIGH)
        GPIO.output(self.clock_enable, GPIO.LOW)

        bytes_val = 0
        for i in range(self.datawidth):
            bit = GPIO.input(self.data)
            bytes_val |= bit << (self.datawidth - 1 - i)

            # Pulse the clock: rising edge shifts the next bit.
            GPIO.output(self.clock, GPIO.HIGH)
            time.sleep(SN74LS165.pulse_time)
            GPIO.output(self.clock, GPIO.LOW)
            time.sleep(SN74LS165.pulse_time)

        return bytes_val

if __name__ == '__main__':
    # Use GPIO numbering:
    GPIO.setmode(GPIO.BCM)

    # Python has no native way to print binary unsigned numbers. Lame!
    def tobin(data, width=8):
        data_str = bin(data & (2**width-1))[2:].zfill(width)
        return data_str

    # shiftr = CD4021(clock=11, latch=9, data=4)
    shiftr = SN74LS165(clock=11, latch=7, data=9, clock_enable=8)
    try:
        while True:
            # b1 = shiftr.read_one_byte()
            # print(format(b1, '#010b'))
            # bytes = [ shiftr.read_one_byte() ]
            bytes = [ shiftr.read_shift_regs() ]
            print('   '.join([tobin(b, 8) for b in bytes]))
            print('   '.join(["%8x" % b for b in bytes]))

            # Sleep at least .0001 between reads
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()


