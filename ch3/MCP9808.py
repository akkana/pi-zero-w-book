#!/usr/bin/env python

# Read temperature from an MCP9808 using I2C.

import smbus

MCP9808 = 0x18         # The default I2C address of the MCP9808
temp_reg = 0x05        # The temperature register

bus = smbus.SMBus(1)

def read_temperature_c():
    data = bus.read_i2c_block_data(MCP9808, temp_reg)

    # Calculate temperature (see 5.1.3.1 in the datasheet):
    upper_byte = data[0] & 0x1f    # clear flag bits
    lower_byte = data[1]
    if upper_byte & 0x10 == 0x10:  # less than 0C
        upper_byte &= 0x0f
        return 256 - (upper_byte * 16.0 + lower_byte / 16.0)
    else:
        return upper_byte * 16.0 + lower_byte / 16.0

if __name__ == '__main__':
    ctemp = read_temperature_c()
    print("Temperature:  %.2f F (%.2f C)" % (ctemp * 1.8 + 32, ctemp))

