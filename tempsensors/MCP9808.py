#!/usr/bin/env python

# Read temperature from an MCP9808 using I2C on a Raspberry Pi.

import smbus
import time

address = 0x18         # The default I2C address of the MCP9808
temp_reg = 0x05        # The temperature register

bus = smbus.SMBus(1)

while (True):
    # The temperature is the first two bytes read, but the MCP9808
    # will sometimes return two zero bytes if you just sequentially
    # call read_byte. It works more reliably if you read it all
    # as one block.
    data = bus.read_i2c_block_data(address, temp_reg)
    print("Read: 0x%x 0x%x" % (data[0], data[1]))

    # Calculate temperature (see 5.1.3.1 in the datasheet,
    # though it's a little confusing and seems to conflate 32C and 0C):
    ctemp = (((data[0] & 0x0f) << 8) + data[1]) / 16.0
    if data[0] & 0x10:
        ctemp = 256 - ctemp
        # A post in https://www.raspberrypi.org/forums/viewtopic.php?t=40831
        # says this should be  ctemp -= 256,
        # but that isn't what the datasheet seems to say.

    print "Temperature:  %.2f F (%.2f C)" % (ctemp * 1.8 + 32, ctemp)

    time.sleep(2)
