#!/usr/bin/env python

from gpiozero import LED, Button
from time import sleep

led = LED(14)
button = Button(15)

# Blink times in seconds:
shortblink = .1
longblink = .7

for i in range(100):
    # Set the LED pin to high for odd numbers, low for even.
    if i % 2:
        led.on()
    else:
        led.off()

    if button.is_pressed:
        sleep(longblink)
    else:
        sleep(shortblink)

