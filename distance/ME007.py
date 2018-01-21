#!/usr/bin/env python

# Raspberry Pi driver for the ME007 ultrasonic rangefinder
# and similar devices.

# Copyright (C) 2018 Akkana Peck <akkana@shallowsky.com>>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# There are lots of different versions of ME007.
# This circuit also works with ME007Y (the one with the long cable)
# and ME007-ULS (the one in the big plastic housing with a button to
# switch modes: put it in PWM mode, single blinks).
# It DOES NOT work with serial versions of the ME007.

import RPi.GPIO as GPIO
import time

class ME007:
    def __init__(self, trigger=23, echo=24):
        self.GPIO_TRIGGER = trigger
        self.GPIO_ECHO    = echo

        # Use BCM instead of physical pin numbering:
        GPIO.setmode(GPIO.BCM)

        # Set trigger and echo pins as output and input
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)

        # Initialize trigger to high:
        GPIO.output(self.GPIO_TRIGGER, True)

    def measure_distance_cm(self, verbose=False):
        '''Measure a single distance, in cemtimeters.
        '''
        return self.measure_distance_in(verbose) * 2.54

    def measure_distance_in(self, verbose=False):
        '''Measure a single distance, in inches.
        '''
        # Make sure the trigger starts high, then goes low
        # to start a measurement:
        GPIO.output(self.GPIO_TRIGGER, True)
        time.sleep(.01)
        GPIO.output(self.GPIO_TRIGGER, False)

        # Wait for the echo to go high, then low.
        # Time how long it stays high.
        GPIO.wait_for_edge(self.GPIO_ECHO, GPIO.RISING, timeout=1000)
        start = time.time()
        GPIO.wait_for_edge(self.GPIO_ECHO, GPIO.FALLING, timeout=1000)
        stop = time.time()

        # Set the trigger back high since we're no longer measuring.
        GPIO.output(self.GPIO_TRIGGER, True)

        # Convert to inches:
        return (((stop - start) * 34300)/2)*0.393701

    def average_distance_in(self, samples=3, verbose=False):
        tot = 0.0
        for i in xrange(samples):
            tot += self.measure_distance_in(verbose)
            time.sleep(0.1)
        return tot / samples

if __name__ == '__main__':
    try:
        rf = ME007()
        while True:
            print "Distance: %.1f inches" % rf.average_distance_in(verbose=True)
            time.sleep(1)
    except KeyboardInterrupt:
        # User pressed CTRL-C: reset GPIO settings.
        print "Cleaning up ..."
        GPIO.cleanup()

