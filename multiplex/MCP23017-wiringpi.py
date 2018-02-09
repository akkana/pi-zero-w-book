#!/usr/bin/env python

import wiringpi
import time

pin_base = 65       # lowest available starting number is 65
i2c_addr = 0x20     # A0, A1, A2 pins all wired to GND

NUMLEDS = 9

wiringpi.wiringPiSetup()                    # initialise wiringpi
wiringpi.mcp23017Setup(pin_base, i2c_addr)  # set up the pins and i2c address
# Set the first 9 pins to output:
for i in range(NUMLEDS):
    wiringpi.pinMode(pin_base + i, wiringpi.OUTPUT)

# and the tenth to input:
input_pin = pin_base + 15
wiringpi.pinMode(input_pin, wiringpi.INPUT)

wiringpi.pullUpDnControl(input_pin, 2)   # set internal pull-up

# Note: MCP23017 has no internal pull-down, so I used pull-up and inverted
# the button reading logic with a "not"

i = 0
try:
    while True:
        print i
        for j in range(0, NUMLEDS):
            if j == i:
                wiringpi.digitalWrite(pin_base + j, 1)
            else:
                wiringpi.digitalWrite(pin_base + j, 0)

        val = wiringpi.digitalRead(input_pin)
        print("Read %d" % val)

        if val:
            i -= 1
        else:
            i += 1

        if i > NUMLEDS:
            i = 0
        elif i < 0:
            i = NUMLEDS
        time.sleep(.5)

except KeyboardInterrupt:
    print "Interrupt"

finally:
    pass
    # wiringpi.digitalWrite(65, 0) # sets port GPA1 to 0 (0V, off)
    # wiringpi.pinMode(65, 0)      # sets GPIO GPA1 back to input Mode
    # GPB7 is already an input, so no need to change anything


