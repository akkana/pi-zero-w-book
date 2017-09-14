#!/usr/bin/env python

# Control a 4 x 7-segment I2C display, for instance,
# one of the undocumented ebay cheapies with labels like
# Kozig or "Thinking & Creative" or ZT SEG8B4A036A.
#
# Thanks to https://github.com/garlick/pi-ted-envoy,
# where led.c and ztled.c showed how to talk to the LED.

import io, fcntl
import time

class LEDI2C:
    I2C_SLAVE = 0x0703

    def __init__(self, bus, address=0x51):
        self.address = address
        # Open the I2C bus:
        # self.fread  = io.open("/dev/i2c-%d" % bus, "rb",
        #                       buffering=0)
        self.fwrite = io.open("/dev/i2c-%d" % bus, "wb",
                              buffering=0)

        # initialize the device as a slave:
        # fcntl.ioctl(self.fread, self.I2C_SLAVE, self.address)
        fcntl.ioctl(self.fwrite, self.I2C_SLAVE, self.address)

        # Set the address to what it already is:
        # self.fwrite.write(b'\x08\x51\x00\x00')
        # print("Set the address")

        self.sleep_set(False)

    def sleep_set(self, sleep):
        '''Put the display to sleep (if sleep=True) or wake it up (False).
           Sleep is 0xa5, wakeup is 0xa1.
        '''
        cmd = bytearray(b'\x04\xa1\x00\x00\x00')
        if sleep:
            cmd[1] = 0xa5
        self.fwrite.write(cmd)

    def test(self):
        '''Light all the segments in a pattern.
        '''
        for i in range(20):
            for i in range(8):
                val = 1<<i;
                self.write_codes(bytearray([val] * 4))
                time.sleep(.2)
            for j in range(2):
                self.write_codes(b'\xff\xff\xff\xff')
                time.sleep(.5)
                self.write_codes(b'\x80\x80\x80\x80')
                time.sleep(.5)

    def close(self):
        # self.fread.close()
        self.fwrite.close()

    def set_brightness(self, b):
        '''Set brightness, between 0 and 0xff.
        '''
        # Also consider using Python's struct for packed binary data.
        cmd = bytearray(b'\x0a\xff\x00\x00')
        # cmd = bytearray(b'\x51\x0a\xff\x00\x00')
        cmd.insert(1, b)
        self.fwrite.write(cmd)

    def write_codes(self, codes):
        '''Write 4 segment codes to the display.
           The segment bits are:
                    -01-
                   |    |
                  20    02
                   |    |
                    -40-
                   |    |
                  10    04
                   |    |
                    -08-   80
        '''
        # self.fwrite.write(b'\x02\xff\xff\xff\x80')
        for d in codes:
            # print "%02x" % ord(d),
            pass
        print

        buf = bytearray(b'\x02')
        # Append the reversed byte string:
        for d in reversed(codes):
            buf.append(d)

        for d in buf:
            # print "%02x" % ord(d),
            pass
        print

        self.fwrite.write(buf)

    # Hex digits. But you can also send other codes to light other
    # combinations of the segments.
    # Add 0x80 to light the decimal point.
    charset = {
        '0': '\x3f', '1': '\x06', '2': '\x5B', '3': '\x4F', '4': '\x66',
        '5': '\x6D', '6': '\x7D', '7': '\x07', '8': '\x7F', '9': '\x6F',
        'A': '\x77', 'B': '\x7C', 'C': '\x39', 'D': '\x5E',
        'E': '\x79', 'F': '\x71'
    }

    def write_string(self, digits):
        '''Write 4 digits to the display.
           Add a . after a character to light its decimal point.
        '''
        buf = bytearray(b'\x51\x02\x00\x00\x00')
        dot = 0x00
        for d in reversed(digits.upper()):
            if d == '.':
                dot = 0x80
                continue
            buf.append(ord(self.charset[d]) | dot)
            dot = 0x00
        self.fwrite.write(buf)

if __name__ == '__main__':
    led = LEDI2C(1)

    led.set_brightness(0x60)

    # led_write_string('12.e.f')
    led.test()

    led.close()



