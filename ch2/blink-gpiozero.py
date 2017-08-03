#!/usr/bin/env python

# Blink an LED using the gpiozero library.

from gpiozero import LED
from time import sleep

# The LED is on pin GPIO 14:
led = LED(14)

# Now blink.
while True:
    led.on()
    sleep(.5)
    led.off()
    sleep(.5)

