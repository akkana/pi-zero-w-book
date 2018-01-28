#!/usr/bin/env python

from __future__ import print_function

# Use three stacked CD4021 shift registers to read a toy keyboard
# and play music using play_chord.py.

# Thanks to WiringPi for the demo of how to use the shift registers:
# https://github.com/WiringPi/WiringPi/blob/9a8f8bee5df60061645918231110a7c2e4d3fa6b/devLib/piNes.c

import RPi.GPIO as GPIO
import sys, os
import time

# Import music playing stuff
sys.path.insert(1, os.path.join(sys.path[0], '../../scripts'))
import play_chord

class CD4021:
    pulseTime = .0025     # gordonDrogon says 25 microseconds, .000025

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
        time.sleep(CD4021.pulseTime)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(CD4021.pulseTime)

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

    def read_n_threebytes(self, nthreebytes):
        threebytes = [ self.read_one_byte() ]

        for i in range(1, nthreebytes):
            # For subsequent threebytes, we don't want another latch but
            # read_byte doesn't start with a clock pulse, so do it here.
            self.pulse_pin(self.clock)
            threebytes.append(self.read_byte())

        return threebytes

# Which note corresponds to which byte and bit:
bytes_to_notes = [
    [
        "G",    # 0x1
        "G#",   # 0x2
        "A",    # 0x4
        "A#",   # 0x8
        "C2",    # 0x10
        "C#2",   # 0x20
        "D2",    # 0x40
        "B2"     # 0x80
    ],
    [
        "F#2",   # 0x1
        "F2",    # 0x2
        "E2",    # 0x4
        "D#2",   # 0x8
        "A#2",   # 0x10
        "A2",    # 0x20
        "G#2",   # 0x40
        "G2"     # 0x80
    ],
    [
        "F3",    # 0x1
        "E3",    # 0x2
        "D#3",   # 0x4
        "D3",    # 0x8
        "C3",    # 0x10
        "B3",    # 0x20
        "NONE",  # 0x40
        "C#3"    # 0x80
    ]
]

def bits(number):
    bit = 1
    i = 0
    while number >= bit:
       if number & bit:
           yield i
       bit <<= 1
       i += 1

def play_notes(threebytes):
    notes = []
    for i, thisbyte in enumerate(threebytes):
        if not thisbyte:
            continue
        # Loop over the bits in thisbyte:
        for bitno in bits(thisbyte):
            notes.append(bytes_to_notes[i][bitno])

    # print("Notes:", notes)

    # Now convert to the format play_notes wants, e.g. "D,B2"
    play_chord.play_notes(','.join(notes))

if __name__ == '__main__':
    shiftr = CD4021(11, 9, 4)

    play_chord.init()

    try:
        while True:
            # b1 = shiftr.read_one_byte()
            # print(format(b1, '#010b'))
            threebytes = shiftr.read_n_threebytes(3)
            # print('   '.join([format(b, '#010b') for b in threebytes]))
            # print('   '.join(["%10x" % b for b in threebytes]))
            play_notes(threebytes)
            # time.sleep(1)

    except KeyboardInterrupt:
        GPIO.cleanup()


