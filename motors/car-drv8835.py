#!/usr/bin/env python

# Drive a car using the Pololu DRV8835 dual motor driver,
# https://www.pololu.com/product/2753/resources

# Requires https://github.com/pololu/drv8835-motor-driver-rpi
# which requires:
# sudo apt-get install wiringpi python-dev python-pip
# sudo pip install wiringpi

import os
import sys
import time
from pololu_drv8835_rpi import motors, MAX_SPEED

FAST_SPEED = 100
SLOW_SPEED = 60

speed1 = 0
speed2 = 0

def accelerate_to(s1, s2):
    global speed1, speed2
    delay = .1
    time.sleep(delay*2)
    for i in range(10):
        motors.setSpeeds((speed1 * (10-i) + s1 * i) / 10,
                         (speed2 * (10-i) + s2 * i) / 10)
        time.sleep(delay)

    speed1 = s1
    speed2 = s2

def stop_now():
    global speed1, speed2
    motors.setSpeeds(0, 0)
    speed1 = 0
    speed2 = 0

if __name__ == '__main__':
    if os.getuid() != 0:
        print("PWM needs root")
        sys.exit(1)
    try:
        accelerate_to(0, 0)
        while True:
            cmd = raw_input("Command: ")
            if cmd.startswith('f'):
                accelerate_to(FAST_SPEED, FAST_SPEED)

            elif cmd.startswith('b'):
                accelerate_to(-SLOW_SPEED, -SLOW_SPEED)

            elif cmd.startswith('l'):
                accelerate_to(FAST_SPEED, SLOW_SPEED)

            elif cmd.startswith('r'):
                accelerate_to(SLOW_SPEED, FAST_SPEED)

            elif cmd.startswith('s'):
                stop_now()

            elif cmd.startswith('q'):
                break

            else:
                accelerate_to(0, 0)
            time.sleep(1)

    finally:
        # In case of problems or user hit ^C, stop both motors.
        accelerate_to(0, 0)
