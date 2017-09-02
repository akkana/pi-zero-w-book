#!/usr/bin/env python

# Control a 28BYJ stepper motor with a ULN2003A driver.
# Adapted from https://tutorials-raspberrypi.com/how-to-control-a-stepper-motor-with-raspberry-pi-and-l293d-uln2003a/

import RPi.GPIO as GPIO
import time

class Stepper_28BYJ:
    # Half-step mode for the 28BYJ has an 8-step control sequence.
    halfstep = [
        [0,1,0,0], [0,1,0,1], [0,0,0,1], [1,0,0,1],
        [1,0,0,0], [1,0,1,0], [0,0,1,0], [0,1,1,0]
        ]

    def __init__(self, a1pin, a2pin, b1pin, b2pin):
        self.a1pin = a1pin    # pink
        self.a2pin = a2pin    # orange
        self.b1pin = b1pin    # blue
        self.b2pin = b2pin    # yellow

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.a1pin, GPIO.OUT)
        GPIO.setup(self.a2pin, GPIO.OUT)
        GPIO.setup(self.b1pin, GPIO.OUT)
        GPIO.setup(self.b2pin, GPIO.OUT)

    def set_step(self, w1, w2, w3, w4):
        GPIO.output(self.a1pin, w1)
        GPIO.output(self.a2pin, w2)
        GPIO.output(self.b1pin, w3)
        GPIO.output(self.b2pin, w4)

    def forward(self, delay, steps):
        for i in range(steps):
            for step in self.halfstep:
                self.set_step(*step)
                time.sleep(delay)

    def backward(self, delay, steps):
        for i in range(steps):
            for step in reversed(self.halfstep):
                self.set_step(*step)
                time.sleep(delay)

    def cleanup(self):
        GPIO.cleanup()

if __name__ == '__main__':
    # Initialize the stepper with 4 GPIO pin numbers.
    # 19, 6, 13, 5 is a sequence that allows plugging the controller
    # board directly into the breadboard next to the Pi Cobbler.
    stepper = Stepper_28BYJ(19, 6, 13, 5)

    # Run the motor forward and backward, as a demo:
    try:
        while True:
            delay = 5./1000.
            steps = 100
            stepper.forward(delay, steps)
            time.sleep(.1)
            stepper.backward(delay, steps)
            time.sleep(.1)
    except KeyboardInterrupt:
        print("Cleaning up")
        stepper.cleanup()

