#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep

# Use Raspberry Pi board pin numbers:
GPIO.setmode(GPIO.BCM)

ledpin = 14
buttonpin = 15

# Blink times in seconds:
shortblink = .1
longblink = .7

# set up GPIO output channel
GPIO.setup(ledpin, GPIO.OUT)
GPIO.setup(buttonpin, GPIO.IN)

for i in range(100):
    # Set the LED pin to high for odd numbers, low for even.
    if i % 2:
        GPIO.output(ledpin, GPIO.HIGH)
    else:
        GPIO.output(ledpin, GPIO.LOW)

    # Sleep for a short time if the button is pressed, otherwise a long time:
    if GPIO.input(buttonpin):
        sleep(shortblink)
    else:
        sleep(longblink)

# Done: clean up!
GPIO.cleanup()
