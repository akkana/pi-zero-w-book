#!/usr/bin/env python

# Blink an LED using the RPi.GPIO library.

import RPi.GPIO as GPIO
from time import sleep

# Use GPIO numbering:
GPIO.setmode(GPIO.BCM)

# Set pin GPIO 14 to be output:
GPIO.setup(14, GPIO.OUT)

try:
    while True:
        GPIO.output(14, GPIO.HIGH)
        sleep(.5)
        GPIO.output(14, GPIO.LOW)
        sleep(.5)

# If we get a Ctrl-C, clean up so we don't get warnings from other programs:
except KeyboardInterrupt:
    GPIO.cleanup()
