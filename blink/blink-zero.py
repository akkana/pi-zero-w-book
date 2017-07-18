#!/usr/bin/env python

from gpiozero import LED
from time import sleep

led = LED(14)

try:
    while True:
        led.on()
        sleep(.5)
        led.off()
        sleep(.5)

except KeyboardInterrupt:
    print("Bye!")

