#!/usr/bin/env python

from __future__ import print_function

# Use three stacked CD4021 shift registers to read a toy keyboard
# and play music using chordplayer.py.

# Thanks to WiringPi for the demo of how to use the shift registers:
# https://github.com/WiringPi/WiringPi/blob/9a8f8bee5df60061645918231110a7c2e4d3fa6b/devLib/piNes.c

import RPi.GPIO as GPIO
import sys, os

# from CD4021 import CD4021
import MCP23017

import noteplayer

# List of frequencies in order -- the MCP23017 version has simpler wiring
freqs = [
    noteplayer.G,
    noteplayer.Ab * 2,
    noteplayer.A * 2,
    noteplayer.Bb * 2,
    noteplayer.B * 2,
    noteplayer.C * 2,
    noteplayer.Db * 2,
    noteplayer.D * 2,

    noteplayer.Eb * 2,
    noteplayer.E * 2,
    noteplayer.F * 2,
    noteplayer.Gb * 2,
    noteplayer.G * 2,
    noteplayer.Ab * 4,  # This is playing as Eb * 2
    noteplayer.A * 4,
    noteplayer.Bb * 4,

    noteplayer.B * 4,
    noteplayer.C * 4,
    noteplayer.Db * 4,
    noteplayer.D * 4,
    noteplayer.Eb * 4,
    noteplayer.E * 4,
    noteplayer.F * 4,
]

def bits(number):
    '''Given a number, returns a list of the bit positions that are on.
       e.g. bits(5) will yield 0, 2.
    '''
    bit = 1
    i = 0
    while number >= bit:
       if number & bit:
           yield i
       bit <<= 1
       i += 1

last_keyboard = None
cur_notes = []

def play_notes(bytes):
    '''bytes is a list of bytes representing which keys are pressed.
       The low-order bit of bytes[0] is the leftmost (lowest) key.
    '''
    global cur_notes, last_keyboard

    changed = False

    if not last_keyboard:
        last_keyboard = [ 0 for b in bytes ]

    # What bits are newly on that weren't on last time?
    for i, thisbyte in enumerate(bytes):
        nowon = thisbyte & ~last_keyboard[i]
        # Loop over the switched-off bits:
        for bitno in bits(nowon):
            freq = freqs[i * 8 + bitno]
            if freq not in cur_notes:
                changed = True
                noteplayer.start_note(freq)

    # What bits were on last time that are off now?
    for i, thisbyte in enumerate(bytes):
        nowoff = ~thisbyte & last_keyboard[i]
        # Loop over the switched-off bits:
        for bitno in bits(nowoff):
            freq = freqs[i * 8 + bitno]
            if freq not in cur_notes:
                changed = True
                noteplayer.stop_note(freq)

    last_keyboard = bytes

    if changed:
        noteplayer.play_current_waves()

if __name__ == '__main__':
    # Use GPIO numbering:
    # GPIO.setmode(GPIO.BCM)

    # mpx = CD4021(11, 9, 4)
    mpx = MCP23017.MCP23017input(MCP23017.BASE_ADDR, MCP23017.BASE_ADDR+1,
                                 pullup=True)
    '''If all three lines are tied high, the second chip shows up at 27
       as expected.
    lines    addr
    111      27
    101      21
    001      --
    '''

    noteplayer.init()

    try:
        while True:
            bytes = mpx.read_n_bytes(3)
            play_notes(bytes)

    except KeyboardInterrupt:
        print("Interrupt")

    finally:
        print("Cleanup")
        noteplayer.stop()
        # GPIO.cleanup()


