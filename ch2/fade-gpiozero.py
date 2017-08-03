#!/usr/bin/env python

# Fade an LED using the gpiozero library.

from gpiozero import PWMLED
from time import sleep

# The LED is on pin 14:
led = PWMLED(14)

value = 0            # Current brightness of the LED
increment = .02      # How much we'll change it each time
sleeptime = .03      # Fraction of a second to sleep each time

try:
    while True:
        value += increment
        # If we're at full brightness, go back to zero.
        if value > 1:
            value = 0
        led.value = value
        sleep(sleeptime)

except KeyboardInterrupt:
    print("Bye!")
