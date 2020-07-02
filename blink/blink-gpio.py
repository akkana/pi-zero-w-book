#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

ledpin = 17

GPIO.setup(ledpin, GPIO.OUT)

try:
    while True:
        GPIO.output(ledpin, GPIO.HIGH)
        sleep(.5)
        GPIO.output(ledpin, GPIO.LOW)
        sleep(.5)

except KeyboardInterrupt:
    GPIO.cleanup()
