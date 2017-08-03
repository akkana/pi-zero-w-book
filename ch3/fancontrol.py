#!/usr/bin/env python

# Control a fan or air conditioner using temperature sensor readings

import RPi.GPIO as GPIO
import smbus
from time import sleep

# Constants:
MCP9808 = 0x18         # The default I2C address of the MCP9808
TEMP_REG = 0x05        # The temperature register

POWERSWITCH = 14       # GPIO pin for the PowerSwitch Tail

# Depending on your PowerSwitch Tail model, you might need to reverse these:
FAN_ON = GPIO.HIGH
FAN_OFF = GPIO.LOW

# How hot does it have to get before turning on a fan?
TOO_HOT = 80

# How many seconds should we sleep between temperature checks?
SLEEPTIME = 60 * 5

bus = smbus.SMBus(1)

def initialize():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(POWERSWITCH, GPIO.OUT)

def get_temperature_f():
    "Return temperature in Fahrenheit"
    data = bus.read_i2c_block_data(MCP9808, TEMP_REG)

    # Calculate temperature (see 5.1.3.1 in the datasheet):
    upper_byte = data[0] & 0x1f    # clear flag bits
    lower_byte = data[1]
    if upper_byte & 0x10 == 0x10:  # less than 0C
        upper_byte &= 0x0f
        ctemp = 256 - (upper_byte * 16.0 + lower_byte / 16.0)
    else:
        ctemp = upper_byte * 16.0 + lower_byte / 16.0

    print(ctemp * 1.8 + 32)
    return ctemp * 1.8 + 32

if __name__ == "__main__":
    initialize()

    try:
        while True:
            temp = get_temperature_f()
            if temp >= TOO_HOT:
                GPIO.output(POWERSWITCH, FAN_ON)
            else:
                GPIO.output(POWERSWITCH, FAN_OFF)

            sleep(SLEEPTIME)
    except KeyboardInterrupt:
        GPIO.cleanup()
