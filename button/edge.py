#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

def button_handler(pin):
    # Since we specified bouncetime, we have to wait a little
    # before checking the pin's value; RPi.GPIO doesn't wait
    # for the pin to settle before calling the event handler.
    # But the amount we need to wait isn't the same as the bounce time.
    # If we wait the full bouncetime, we'll get multiple events.
    time.sleep(.01)
    if GPIO.input(pin):
        print("ON")
    else:
        print("OFF")

if __name__ == '__main__':
    button_pin = 18

    GPIO.setmode(GPIO.BCM)

    # Wire the button to +3.3, then enable an internal pulldown.
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # events can be GPIO.RISING, GPIO.FALLING, or GPIO.BOTH
    GPIO.add_event_detect(button_pin, GPIO.BOTH, callback=button_handler,
                          bouncetime=300)

    try:
        time.sleep(1000)
    except KeyboardInterrupt:
        print("Interrupt")
    finally:
        GPIO.cleanup()

