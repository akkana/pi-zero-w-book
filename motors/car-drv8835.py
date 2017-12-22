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
import termios
import fcntl
import tty
import select
from pololu_drv8835_rpi import motors, MAX_SPEED

class Car8835:
    FAST_SPEED = 100
    SLOW_SPEED = 60

    def __init__(self):
        self.speed1 = 0
        self.speed2 = 0

    def accelerate_to(self, s1, s2):
        global speed1, speed2
        delay = .1
        time.sleep(delay*2)
        for i in range(10):
            motors.setSpeeds((self.speed1 * (10-i) + s1 * i) / 10,
                             (self.speed2 * (10-i) + s2 * i) / 10)
            time.sleep(delay)

        self.speed1 = s1
        self.speed2 = s2

    def stop_now(self):
        motors.setSpeeds(0, 0)
        self.speed1 = 0
        self.speed2 = 0

class raw(object):
    def __init__(self, stream):
        self.stream = stream
        self.fd = self.stream.fileno()
    def __enter__(self):
        self.original_stty = termios.tcgetattr(self.stream)
        tty.setcbreak(self.stream)
    def __exit__(self, type, value, traceback):
        termios.tcsetattr(self.stream, termios.TCSANOW, self.original_stty)

class nonblocking(object):
    def __init__(self, stream):
        self.stream = stream
        self.fd = self.stream.fileno()
    def __enter__(self):
        self.orig_fl = fcntl.fcntl(self.fd, fcntl.F_GETFL)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl | os.O_NONBLOCK)
    def __exit__(self, *args):
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl)

if __name__ == '__main__':
    if os.getuid() != 0:
        print("PWM needs root")
        sys.exit(1)

    try:
        car = Car8835()
        car.accelerate_to(0, 0)

        with raw(sys.stdin):
            with nonblocking(sys.stdin):

                while True:
                    r, w, e = select.select([sys.stdin], [], [])
                    if r:
                        cmd = sys.stdin.read()

                        if cmd.startswith('f'):
                            car.accelerate_to(Car8835.FAST_SPEED, Car8835.FAST_SPEED)

                        elif cmd.startswith('b'):
                            car.accelerate_to(-Car8835.SLOW_SPEED, -Car8835.SLOW_SPEED)

                        elif cmd.startswith('l'):
                            car.accelerate_to(Car8835.FAST_SPEED, Car8835.SLOW_SPEED)

                        elif cmd.startswith('r'):
                            car.accelerate_to(Car8835.SLOW_SPEED, Car8835.FAST_SPEED)

                        elif cmd.startswith('s'):
                            car.stop_now()

                        elif cmd.startswith('q'):
                            break

                        else:
                            car.accelerate_to(0, 0)

                        time.sleep(1)

    finally:
        # In case of problems or user hit ^C, stop both motors.
        car.accelerate_to(0, 0)
