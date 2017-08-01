#!/usr/bin/env python

# Read temperature and humidity from an Si7021 using I2C on a Raspberry Pi.
# smbus doesn't work for this chip, so try direct I/O to the device.

import time
import array
import io
import fcntl

class Si7021:
    ADDRESS = 0x40
    I2C_SLAVE=0x0703
    READ_TEMP_HOLD = "\xE3"
    READ_TEMP_NOHOLD = "\xF3"
    READ_HUM_HOLD = "\xE5"
    READ_HUM_NOHOLD = "\xF5"
    SOFT_RESET = "\xFE"

    def __init__(self, bus):
        # Open the I2C bus:
        self.fread  = io.open("/dev/i2c-%d" % bus, "rb", buffering=0)
        self.fwrite = io.open("/dev/i2c-%d" % bus, "wb", buffering=0)

        # initialize the device as a slave:
        fcntl.ioctl(self.fread, self.I2C_SLAVE, self.ADDRESS)
        fcntl.ioctl(self.fwrite, self.I2C_SLAVE, self.ADDRESS)

        self.fwrite.write(self.SOFT_RESET)    # soft reset
        time.sleep(.1)

    def close(self):
        self.fread.close()
        self.fwrite.close()

    def readI2C(self, cmd):
        # These give errors:
        # data = self.bus.read_i2c_block_data(self.address, cmd)
        # word = self.bus.read_word_data(self.address, cmd)
        # This works to read the first byte,
        # but the second byte read is just a repeat of the first:
        # self.bus.write_byte(self.address, cmd)
        # time.sleep(self.pausetime)
        # byte0 = self.bus.read_byte(self.address)
        # time.sleep(self.pausetime)
        # byte1 = self.bus.read_byte(self.address)

        # So instead, read/write directly from/to the /dev/i2c* device.
        self.fwrite.write(cmd)
        time.sleep(.1)

        data = self.fread.read(3)
        buf = array.array('B', data)

        if self.crc8check(buf):
            return buf
        else:
            return None

    def read_temperature_c(self):
        buf = self.readI2C(self.READ_TEMP_NOHOLD)
        if not buf:
            return -273.15    # absolute zero

        return ((buf[0] << 8 | buf [1]) & 0xFFFC) * 175.72 / 65536.0 - 46.85

    def read_humidity(self):
        buf = self.readI2C(self.READ_HUM_NOHOLD)
        if not buf:
            return -1

        return ((buf[0] << 8 | buf [1]) & 0xFFFC) * 125.0 / 65536.0 - 6.0

        # return ((hum0 * 256 + hum1) * 125 / 65536.0) - 6

    def crc8check(self, value):
        # Ported from the Sparkfun Arduino HTU21D Library,
        # https://github.com/sparkfun/HTU21D_Breakout, by way of
        # https://www.raspberrypi.org/forums/viewtopic.php?f=44&t=76688
        remainder = ( ( value[0] << 8 ) + value[1] ) << 8
        remainder |= value[2]

        # POLYNOMIAL = 0x0131 = x^8 + x^5 + x^4 + 1
        # divsor = 0x988000 is the 0x0131 polynomial shifted
        # to farthest left of three bytes
        divsor = 0x988000

        for i in range(0, 16):
            if( remainder & 1 << (23 - i) ):
                remainder ^= divsor
            divsor = divsor >> 1

        if remainder == 0:
            return True
        else:
            return False

if __name__ == '__main__':
    sensor = Si7021(1)
    ctemp = sensor.read_temperature_c()
    print "Temperature:  %.2f F (%.2f C)" % (ctemp * 1.8 + 32, ctemp)
    print "Relative Humidity: %.1f %%" % sensor.read_humidity()
    sensor.close()

