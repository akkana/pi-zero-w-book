#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

def button_handler(pin):
    # There seems to be a delay between the time a FALLING event is called
    # and when GPIO.input can actually read the button as low.
    # Empirically, .001 isn't enough to read it reliably, but .01 seems to be.
    time.sleep(.01)
    if GPIO.input(pin):
        print("ON")
    else:
        print("OFF")

if __name__ == '__main__':
    button_pin = 18

    GPIO.setmode(GPIO.BCM)

    # Wire the button to +3.3, then enable an internal pulldown.
    GPIO.setup(button_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    # events can be GPIO.RISING, GPIO.FALLING, or GPIO.BOTH
    GPIO.add_event_detect(button_pin, GPIO.BOTH,
                          callback=button_handler,
                          bouncetime=300)

    time.sleep(1000)

