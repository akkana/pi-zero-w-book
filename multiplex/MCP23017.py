#!/usr/bin/env python

from __future__ import print_function

# https://www.raspberrypi-spy.co.uk/2013/07/how-to-use-a-mcp23017-i2c-port-expander-with-the-raspberry-pi-part-1/
# https://www.raspberrypi-spy.co.uk/2013/07/how-to-use-a-mcp23017-i2c-port-expander-with-the-raspberry-pi-part-2/
# https://www.raspberrypi-spy.co.uk/2013/07/how-to-use-a-mcp23017-i2c-port-expander-with-the-raspberry-pi-part-3/

# Also (less good),
# https://learn.adafruit.com/mcp230xx-gpio-expander-on-the-raspberry-pi?view=all
# https://www.mathworks.com/help/supportpkg/raspberrypiio/examples/add-digital-i-o-pins-to-raspberry-pi-hardware-using-mcp23017.html?requestedDomain=true

import smbus

BASE_ADDR = 0x20 # Device address (A0-A2)

# Commands to send to the MCP23017 for the two GPs of 8 pins each:
IODIRA = 0x00    # Direction for GPA
IODIRB = 0x01    # Direction for GPB
GPIOA  = 0x12    # Input from GPA
GPIOB  = 0x13    # Input from GPB
OLATA  = 0x14    # Output to GPA
OLATB  = 0x15    # Output to GPB
GPPUA  = 0x0c    # Pullup resistor on GPA
GPPUB  = 0x0d    # Pullup resistor on GPB

class MCP23017input:
    def __init__(*args, **kwargs):
        '''Args are self, addr[, addr, ...]
           kwargs may include pullup=True (which will apply to all pins).
           If pullupts are enabled, we'll invert the output.
        '''
        self = args[0]
        self.bus = smbus.SMBus(1)     # Pi 3 and Zero use 1, 1 uses 0
        self.addrs = args[1:]
        self.invert = False

        # If requested, enable all internal pullups:
        if 'pullup' in kwargs and kwargs['pullup']:
            print("Enabling pullups")
            self.invert = True
            for chip in self.addrs:
                self.bus.write_byte_data(chip, GPPUA, 0xff)
                self.bus.write_byte_data(chip, GPPUB, 0xff)

    def read_n_bytes(self, nbytes):
        if nbytes > len(self.addrs) * 2:
            raise RuntimeError("Requested %d bytes, only initialized %d chips" \
                               % (nbytes, len(self.addrs)))
        bytes = []
        for chip in self.addrs:
            val = self.bus.read_byte_data(chip, GPIOA)
            # print("Read 0x%x from chip 0x%x SDA" % (val, chip))
            if self.invert:
                # Python's ~ is useless, always adds a sign bit. ^ works better.
                val = val ^ 0xff
            bytes.append(val)
            nbytes -= 1
            if not nbytes:
                return bytes
            val = self.bus.read_byte_data(chip, GPIOB)
            # print("Read 0x%x from chip 0x%x SDB" % (val, chip))
            if self.invert:
                val = val ^ 0xff
            bytes.append(val)
            nbytes -= 1
            if not nbytes:
                return bytes

if __name__ == '__main__':
    import time

    def tobin(data, width=8):
        data_str = bin(data & (2**width-1))[2:].zfill(width)
        return data_str

    chip = MCP23017input(BASE_ADDR, BASE_ADDR+1, pullup=True)
    try:
        while True:
            bytes = chip.read_n_bytes(3)
            print("Read: ", end='')
            for byte in bytes:
                print("0x%02x (%s)  " % (byte, tobin(byte)), end='')
            print()
            time.sleep(1)

    except KeyboardInterrupt:
        print("Interrupt")


