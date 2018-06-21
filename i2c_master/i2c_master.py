#!/usr/bin/env python

# Compatibility with both python2 and python3:
from __future__ import print_function
if hasattr(__builtins__, 'raw_input'):
    input = raw_input

# Very simple I2C demo that can be used to talk to an Arduino using I2C.
# For the Arduino side of the code, see:
# https://github.com/akkana/arduino/tree/master/i2c_client

import smbus
import time
import sys

# The I2C address the Arduino will use
address = 0x04

def initBus():
    # Initialize I2C. For Pi 1, use "bus = smbus.SMBus(0)"
    bus = smbus.SMBus(1)

    # Delay to make sure the I2C bus will be ready,
    # otherwise you might see an IOError exception.
    time.sleep(1)

    return bus

def writeByte(value):
    bus.write_byte(address, value)
    # bus.write_byte_data(address, 0, value)

def readByte():
    number = bus.read_byte(address)
    return number

def read2Bytes():
    # The second argument of read_word_data() is cmd.
    # It's optional for read_byte but mandatory for read_word_data.
    # The documentation doesn't say what it is or how it's sent,
    # but on the Arduino end, you can wait for a Wire.onReceive
    # and then call = Wire.read();
    # (ideally in a loop, but there will be only one byte).
    number = bus.read_word_data(address, 1)
    return number

# Be cautious of read_i2c_block_data(), it can hang the RPi,
# requiring a power cycle.

if __name__ == '__main__':
    bus = initBus()

    while True:
        try:
            cnd = input("q to quit, anything else will read data: ")
            if cnd == 'q':
                sys.exit(0)
        except NameError:
            print("Need an integer")
            continue

        val = read2Bytes()
        print("Read:", val)


