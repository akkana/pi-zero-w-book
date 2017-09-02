#!/usr/bin/env python

# Control a 28BYJ stepper motor with a L293D or ULN2003A driver.
# From https://tutorials-raspberrypi.com/how-to-control-a-stepper-motor-with-raspberry-pi-and-l293d-uln2003a/
# Arduino version:
# http://42bots.com/tutorials/28byj-48-stepper-motor-with-uln2003-driver-and-arduino-uno/
#
# There's also this: https://www.pololu.com/product/2753
# but it can run one bipolar stepper, and the 28BYJ is unipolar.

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# coil_A_1_pin = 4 # pink
# coil_A_2_pin = 17 # orange
# coil_B_1_pin = 23 # blue
# coil_B_2_pin = 24 # yellow

coil_A_1_pin = 19 # pink
coil_A_2_pin =  6 # orange
coil_B_1_pin = 13 # blue
coil_B_2_pin =  5 # yellow

# adjust if different
StepCount = 8
Seq = range(0, StepCount)
Seq[0] = [0,1,0,0]
Seq[1] = [0,1,0,1]
Seq[2] = [0,0,0,1]
Seq[3] = [1,0,0,1]
Seq[4] = [1,0,0,0]
Seq[5] = [1,0,1,0]
Seq[6] = [0,0,1,0]
Seq[7] = [0,1,1,0]

# GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

# GPIO.output(enable_pin, 1)

def setStep(w1, w2, w3, w4):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_A_2_pin, w2)
    GPIO.output(coil_B_1_pin, w3)
    GPIO.output(coil_B_2_pin, w4)

def forward(delay, steps):
    for i in range(steps):
        for j in range(StepCount):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)

def backwards(delay, steps):
    for i in range(steps):
        for j in reversed(range(StepCount)):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)

if __name__ == '__main__':
    while True:
        # delay = raw_input("Time Delay (ms)?")
        # steps = raw_input("How many steps forward? ")
        delay = 5
        steps = 100
        forward(int(delay) / 1000.0, int(steps))
        time.sleep(.1)
        backwards(int(delay) / 1000.0, int(steps))
        time.sleep(.1)

