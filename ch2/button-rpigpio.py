#!/usr/bin/env python

# Adjust blinking LED according to whether a button is pressed.

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
    if i % 2:
        # If i is odd, turn the LED on
        GPIO.output(ledpin, GPIO.HIGH)
    else:
        # If i is even, turn the LED on
        GPIO.output(ledpin, GPIO.LOW)

    # Sleep for a short time if the button is pressed, otherwise a long time:
    if GPIO.input(buttonpin):
        sleep(shortblink)
    else:
        sleep(longblink)

# Done: clean up!
GPIO.cleanup()
