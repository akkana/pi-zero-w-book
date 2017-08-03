#!/usr/bin/env python

# Adjust blinking LED according to whether a button is pressed.

from gpiozero import LED, Button
from time import sleep

led = LED(14)
button = Button(15)

# Blink times in seconds:
shortblink = .1
longblink = .7

for i in range(100):
    if i % 2:
        # If i is odd, turn the LED on
        led.on()
    else:
        # If i is even, turn the LED off
        led.off()

    # Sleep for a short time if the button is pressed, otherwise a long time:
    if button.is_pressed:
        sleep(shortblink)
    else:
        sleep(longblink)


