#!/usr/bin/env python3

#
# Monitor soil moisture, and water a plant as it needs it.
#
# Copyright 2020 by Akkana Peck: share and enjoy under the GPL v2 or later.
#

# ADS1115 ADC notes:
# https://github.com/adafruit/Adafruit_CircuitPython_ADS1x15
# chan.value goes from 0 - 26512
# chan.voltage    from 0 - 3.314

# Values read from the YL-38 moisture sensor via the ADS1115
# dry soil:    26480  3.310
# better:      14528  1.816
# soggy:       12576  1.572
# swishing around in the water: 7216  0.902
# then settles back to soggy 12000  1.502
TOO_DRY = 20000

import time
import RPi.GPIO as GPIO
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# How long to run the pump, and at what duty cycle:
PUMP_DURATION = 3    # seconds
PUMP_DUTY = 30

# When did the pump last fire?
last_pumped = 0

# How long to wait between pumps for the soil to equalize (secs)
soil_wait_time = 30

PUMP_PIN = 23

#
# Initialize the ADC that will be used to read the moisture sensor:
#

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended input on adc0nel 0
adc0 = AnalogIn(ads, ADS.P0)

# Create differential input between adc0nel 0 and 1
#adc0 = AnalogIn(ads, ADS.P0, ADS.P1)

#
# Initialize the water pump,
# a small  motor used via PWM on a SN754410 H-bridge chip.
#
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
pump = GPIO.PWM(PUMP_PIN, 50)
pump.start(0)

#
# Main Loop. Break with Ctrl-C.
#

try:
    while True:
        value = adc0.value
        if value > TOO_DRY:
            print(f'TOO DRY! {value}  {adc0.voltage:>5.3f}')

            if time.time() - last_pumped > soil_wait_time:
                print("Watering ...")
                pump.ChangeDutyCycle(PUMP_DUTY)
                time.sleep(PUMP_DURATION)
                pump.ChangeDutyCycle(0)
                last_pumped = time.time()
        else:
            print(f'{value}  {adc0.voltage:>5.3f}')

        time.sleep(2)

except KeyboardInterrupt:
    pump.stop()
    print("Bye")

