#!/usr/bin/env python

# Read temperature and humidity from an Si7021 using I2C on a Raspberry Pi.

import smbus
import time

class Si7021:
    address = 0x40
    pausetime = 0.3
    READ_TEMP = 0xF3
    READ_HUMIDITY = 0xF5

    def __init__(self):
        self.bus = smbus.SMBus(1)
        time.sleep(self.pausetime)

    def readI2C(self, code):
        # Doesn't work:
        # data = self.bus.read_i2c_block_data(self.address, code)
        # print "data", data
        # return data[0:2]

        # Doesn't work:
        # word = self.bus.read_word_data(self.address, code)
        # print "Read word 0x%x" % word
        # byte0 = word & 0xff
        # byte1 = (word % 0xff00) >> 8

        # This works:
        self.bus.write_byte(self.address, code)
        time.sleep(self.pausetime)
        byte0 = self.bus.read_byte(self.address)
        time.sleep(self.pausetime)
        byte1 = self.bus.read_byte(self.address)
        print "Read", byte0, byte1

        return byte0, byte1

    def read_humidity(self):
        hum0, hum1 = self.readI2C(self.READ_HUMIDITY)
        return ((hum0 * 256 + hum1) * 125 / 65536.0) - 6

    def read_temperature(self):
        temp0, temp1 = self.readI2C(self.READ_TEMP)
        return ((temp0 * 256 + temp1) * 175.72 / 65536.0) - 46.85

if __name__ == '__main__':
    sensor = Si7021()
    print "Relative Humidity: %.1f %%" % sensor.read_humidity()
    ctemp = sensor.read_temperature()
    print "Temperature:  %.2f F (%.2f C)" % (ctemp * 1.8 + 32, ctemp)

