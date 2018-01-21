#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

if __name__ == '__main__':
    button_pin = 18

    GPIO.setmode(GPIO.BCM)

    # Wire the button to +3.3, then enable an internal pulldown.
    GPIO.setup(button_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    try:
        while True:
            if GPIO.input(button_pin):
                print("ON")
            else:
                print("OFF")

            time.sleep(2)

    except KeyboardInterrupt:
        print("cleaning up")
        GPIO.cleanup()
