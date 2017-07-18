#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO.setup(14, GPIO.OUT)

try:
    while True:
        GPIO.output(14, GPIO.HIGH)
        sleep(.5)
        GPIO.output(14, GPIO.LOW)
        sleep(.5)

except KeyboardInterrupt:
    GPIO.cleanup()
