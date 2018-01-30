#!/usr/bin/env python

from __future__ import print_function

# Use three stacked CD4021 shift registers to read a toy keyboard
# and play music using chordplayer.py.

# Thanks to WiringPi for the demo of how to use the shift registers:
# https://github.com/WiringPi/WiringPi/blob/9a8f8bee5df60061645918231110a7c2e4d3fa6b/devLib/piNes.c

import RPi.GPIO as GPIO
import sys, os

from CD4021 import CD4021

import noteplayer

# Which bytes and bits corresponds to which frequencies:
bytes_to_freqs = [
    [
        noteplayer.G,        # 0x1
        noteplayer.Ab * 2,   # 0x2
        noteplayer.A * 2,    # 0x4
        noteplayer.Bb * 2,   # 0x8
        noteplayer.C * 2,    # 0x10
        noteplayer.Db * 2,   # 0x20
        noteplayer.D * 2,    # 0x40
        noteplayer.B * 2     # 0x80
    ],
    [
        noteplayer.Gb * 2,   # 0x1
        noteplayer.F * 2,    # 0x2
        noteplayer.E * 2,    # 0x4
        noteplayer.Eb * 2,   # 0x8
        noteplayer.Bb * 4,   # 0x10
        noteplayer.A * 4,    # 0x20
        noteplayer.Ab * 4,   # 0x40
        noteplayer.G * 2     # 0x80
    ],
    [
        noteplayer.D * 4,    # 0x1
        noteplayer.Db * 4,   # 0x2
        noteplayer.C * 4,    # 0x4
        noteplayer.B * 4,    # 0x8
        noteplayer.F * 4,    # 0x10
        noteplayer.Eb * 4,   # 0x20
        None,                # 0x40
        noteplayer.E * 4,    # 0x80
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

last_keyboard = [0, 0, 0]
cur_notes = []

def play_notes(threebytes):
    global cur_notes, last_keyboard

    changed = False

    # What bits are newly on that weren't on last time?
    for i, thisbyte in enumerate(threebytes):
        nowon = thisbyte & ~last_keyboard[i]
        # Loop over the switched-off bits:
        for bitno in bits(nowon):
            freq = bytes_to_freqs[i][bitno]
            if freq not in cur_notes:
                changed = True
                noteplayer.start_note(freq)

    # What bits were on last time that are off now?
    for i, thisbyte in enumerate(threebytes):
        nowoff = ~thisbyte & last_keyboard[i]
        # Loop over the switched-off bits:
        for bitno in bits(nowoff):
            freq = bytes_to_freqs[i][bitno]
            if freq not in cur_notes:
                changed = True
                noteplayer.stop_note(freq)

    last_keyboard = threebytes

    if changed:
        noteplayer.play_current_waves()

if __name__ == '__main__':
    # Use GPIO numbering:
    GPIO.setmode(GPIO.BCM)

    shiftr = CD4021(11, 9, 4)

    noteplayer.init()

    try:
        while True:
            threebytes = shiftr.read_n_bytes(3)
            play_notes(threebytes)

    except KeyboardInterrupt:
        print("Interrupt")

    finally:
        print("Cleanup")
        noteplayer.stop()
        GPIO.cleanup()


