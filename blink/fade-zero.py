#!/usr/bin/env python

# Fade an LED from 0 to 1, then restart at 0, using Pulse-Width Modulation.

from gpiozero import PWMLED
from time import sleep

led = PWMLED(14)   # Raspberry Pi pin 8, GPIO 14

value = 0

increment = .02    # How smooth is the fade?
sleeptime = .03    # How fast is the fade?

# Catch keyboard interrupts, so the gpiozero library can reset the GPIO.
try:
    while True:
        value += increment
        if value > 1:
            value = 0
        led.value = value
        sleep(sleeptime)

except KeyboardInterrupt:
    print("Bye!")
