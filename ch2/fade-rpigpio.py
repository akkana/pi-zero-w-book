#!/usr/bin/env python

# Fade an LED using the gpiozero library.

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO.setup(14, GPIO.OUT)
pwm = GPIO.PWM(14, 100)     # Set up PWM on pin 14 at 100 Hz

value = 0                   # Current brightness of the LED
pwm.start(value)            # Start at 0

increment = 2               # How smooth is the fade?
sleeptime = .03             # How fast is the fade?

try:
    while True:
        value += increment
        if value > 100:
            value = 0
        pwm.ChangeDutyCycle(value)
        sleep(sleeptime)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
