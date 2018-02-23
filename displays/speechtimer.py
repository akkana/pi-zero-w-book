#!/usr/bin/env python

from __future__ import print_function

# This uses https://luma-led-matrix.readthedocs.io/

# Wiring:
# MAX7219	Name 	Remarks 	RPi Pin	RPi Function
# 1 	VCC 	+5V Power 	2 	5V0
# 2 	GND 	Ground 		6 	GND
# 3 	DIN 	Data In 	19 	GPIO 10 (MOSI)   via level shifter
# 4 	CS 	Chip Select 	24 	GPIO 8 (SPI CE0) via level shifter
# 5 	CLK 	Clock 	23 	GPIO 11 (SPI CLK)        via level shifter
# A bidirectional logic level shifter works.

# GPIO pins for green, yellow and red lights:
lightpins = (17, 27, 22)

import time
import sched

import RPi.GPIO as GPIO

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import sevensegment

def gyr(curtime, goaltime, goalmin):
    '''Calculate green, yellow, red booleans.
       depending on the current time and goal time, both in seconds.
    '''
    # This will be called once a second; if we're over the goal time
    # by more than half a minute, the red light should flash,
    # so it will be True on odd seconds, False on even seconds.
    if curtime > goaltime + 30:
        return False, False, (True if (int(curtime) % 2) else False)

    # If we're over time but not by more than half a minute, light the red:
    if curtime > goaltime:
        return False, False, True

    # For times 15 minutes and up, green and yellow get 2.5 minutes each.
    if goalmin >= 15:
        if curtime > goaltime - 150:    # yellow
            return False, True, False
        if curtime > goaltime - 300:      # green
            return True, False, False
        return False, False, False

    # For times 4 minutes and up, green and yellow get 1 minute each.
    if goalmin >= 4:
        if curtime > goaltime - 60:    # yellow
            return False, True, False
        if curtime > goaltime - 120:   # green
            return True, False, False
        return False, False, False

    # Under 4 minutes, each light only gets 30 seconds
    if curtime > goaltime - 30:    # yellow
        return False, True, False
    if curtime > goaltime - 60:    # green
        return True, False, False
    return False, False, False

def tick(scheduler, starttime, goaltime, seg, goalmin):
    now = time.time()
    seconds = int(now - starttime)
    minutes = int(seconds / 60)
    seconds = int(seconds % 60)
    # print("%02d:%02d" % (minutes, seconds))
    seg.text = "%-4d%02d.%02d" % (goalmin, minutes, seconds)
    lights = gyr(now, goaltime, goalmin)
    print("Lights:", lights)
    for i, val in enumerate(lights):
        GPIO.output(lightpins[i], GPIO.HIGH if val else GPIO.LOW)

    # The next time we'll tick. Make it far enough ahead that
    # we won't miss it.
    nexttime = int(time.time() + .3) + 1
    scheduler.enterabs(nexttime, 1, tick,
                       (scheduler, starttime, goaltime, seg, goalmin))

def timeit(minutes, seg):
    scheduler = sched.scheduler(time.time, time.sleep)
    now = time.time()
    tick(scheduler, now, now + minutes * 60, seg, minutes)
    scheduler.run()

if __name__ == '__main__':
    try:
        # create seven segment device
        serial = spi(port=0, device=0, gpio=noop())
        device = max7219(serial, cascaded=1)
        seg = sevensegment(device)

        GPIO.setmode(GPIO.BCM)
        for pin in lightpins:
            GPIO.setup(pin, GPIO.OUT)

        timeit(1, seg)

    except KeyboardInterrupt:
        print("Interrupt")

    finally:
        print("Cleaning up")
        GPIO.cleanup()

