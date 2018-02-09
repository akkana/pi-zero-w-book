#!/usr/bin/env python

# https://www.raspberrypi-spy.co.uk/2013/07/how-to-use-a-mcp23017-i2c-port-expander-with-the-raspberry-pi-part-1/
# https://www.raspberrypi-spy.co.uk/2013/07/how-to-use-a-mcp23017-i2c-port-expander-with-the-raspberry-pi-part-2/
# https://www.raspberrypi-spy.co.uk/2013/07/how-to-use-a-mcp23017-i2c-port-expander-with-the-raspberry-pi-part-3/

# Also (less good),
# https://learn.adafruit.com/mcp230xx-gpio-expander-on-the-raspberry-pi?view=all
# https://www.mathworks.com/help/supportpkg/raspberrypiio/examples/add-digital-i-o-pins-to-raspberry-pi-hardware-using-mcp23017.html?requestedDomain=true

import smbus
import time

#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

DEVICE = 0x20 # Device address (A0-A2)

# Commands to send to the MCP23017 for the two GPs of 8 pins each:
IODIRA = 0x00    # Direction for GPA
IODIRB = 0x01    # Direction for GPB
GPIOA  = 0x12    # Input from GPA
GPIOB  = 0x13    # Input from GPB
OLATA  = 0x14    # Output to GPA
OLATB  = 0x15    # Output to GPB

# Set all GPA pins as outputs by setting all bits of IODIRA register to 0
bus.write_byte_data(DEVICE, IODIRA, 0x00)

# For GPB, set the highest bit to output, the rest to input.
# Need to save the mask because it's needed for reading.
inmaskB = 0x80
bus.write_byte_data(DEVICE, IODIRB, inmaskB)

try:
    number = 1
    while True:
        lownum = number & 0xff
        highnum = (number >> 8) & 0xff
        print("0x%-4x  %4d     0x%-2x  0x%-2x" % (number, number,
                                                  lownum, highnum))

        bus.write_byte_data(DEVICE, OLATA, lownum)
        bus.write_byte_data(DEVICE, OLATB, highnum)

        # When reading, the chip will read all the output channels
        # as well as the ones specified for input, so need to
        # mask the value read with the output mask passed with IODIRB:
        val = bus.read_byte_data(DEVICE, GPIOB) & inmaskB
        print("Read: %d" % val)

        if val:
            number >>= 1
        else:
            number <<= 1

        if number > 0x200:
            number = 1
        elif number == 0:
            number = 0x200
        time.sleep(1)

except KeyboardInterrupt:
    print "Interrupt"

finally:
    print "Cleaning up"
    # Set all bits to zero
    bus.write_byte_data(DEVICE, OLATA, 0)

