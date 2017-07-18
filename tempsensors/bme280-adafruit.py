#!/usr/bin/env python
#coding: utf-8

# Read a BME280 temperature-humidity sensor from a Raspberrry Pi.

# Requires the Adafruit_GPIO.I2C library.

# Adafruit's example code didn't work for me, but this did:
# https://forums.adafruit.com/viewtopic.php?f=19&t=89049

import Adafruit_GPIO.I2C as I2C
import time
i2c = I2C
device=i2c.get_i2c_device(0x77) # address of BMP

# this value is necessary to calculate the correct height above sealevel
# its also included in airport wheather information ATIS named as QNH
# unit is hPa
QNH=1020
print("QNH:{:.0f}".format(QNH)+" hPA")

# power mode
# POWER_MODE=0 # sleep mode
# POWER_MODE=1 # forced mode
# POWER_MODE=2 # forced mode
POWER_MODE=3 # normal mode

# temperature resolution
# OSRS_T = 0 # skipped
# OSRS_T = 1 # 16 Bit
# OSRS_T = 2 # 17 Bit
# OSRS_T = 3 # 18 Bit
# OSRS_T = 4 # 19 Bit
OSRS_T = 5 # 20 Bit

# pressure resolution
# OSRS_P = 0 # pressure measurement skipped
# OSRS_P = 1 # 16 Bit ultra low power
# OSRS_P = 2 # 17 Bit low power
# OSRS_P = 3 # 18 Bit standard resolution
# OSRS_P = 4 # 19 Bit high resolution
OSRS_P = 5 # 20 Bit ultra high resolution

# filter settings
# FILTER = 0 #
# FILTER = 1 #
# FILTER = 2 #
# FILTER = 3 #
FILTER = 4 #
# FILTER = 5 #
# FILTER = 6 #
# FILTER = 7 #

# standby settings
# T_SB = 0 # 000 0,5ms
# T_SB = 1 # 001 62.5 ms
# T_SB = 2 # 010 125 ms
# T_SB = 3 # 011 250ms
T_SB = 4 # 100 500ms
# T_SB = 5 # 101 1000ms
# T_SB = 6 # 110 2000ms
# T_SB = 7 # 111 4000ms


CONFIG = (T_SB <<5) + (FILTER <<2) # combine bits for config
CTRL_MEAS = (OSRS_T <<5) + (OSRS_P <<2) + POWER_MODE # combine bits for ctrl_meas

# print ("CONFIG:",CONFIG)
# print ("CTRL_MEAS:",CTRL_MEAS)

BMP280_REGISTER_DIG_T1 = 0x88
BMP280_REGISTER_DIG_T2 = 0x8A
BMP280_REGISTER_DIG_T3 = 0x8C
BMP280_REGISTER_DIG_P1 = 0x8E
BMP280_REGISTER_DIG_P2 = 0x90
BMP280_REGISTER_DIG_P3 = 0x92
BMP280_REGISTER_DIG_P4 = 0x94
BMP280_REGISTER_DIG_P5 = 0x96
BMP280_REGISTER_DIG_P6 = 0x98
BMP280_REGISTER_DIG_P7 = 0x9A
BMP280_REGISTER_DIG_P8 = 0x9C
BMP280_REGISTER_DIG_P9 = 0x9E
BMP280_REGISTER_CHIPID = 0xD0
BMP280_REGISTER_VERSION = 0xD1
BMP280_REGISTER_SOFTRESET = 0xE0
BMP280_REGISTER_CONTROL = 0xF4
BMP280_REGISTER_CONFIG  = 0xF5
BMP280_REGISTER_STATUS = 0xF3
BMP280_REGISTER_TEMPDATA_MSB = 0xFA
BMP280_REGISTER_TEMPDATA_LSB = 0xFB
BMP280_REGISTER_TEMPDATA_XLSB = 0xFC
BMP280_REGISTER_PRESSDATA_MSB = 0xF7
BMP280_REGISTER_PRESSDATA_LSB = 0xF8
BMP280_REGISTER_PRESSDATA_XLSB = 0xF9

if (device.readS8(BMP280_REGISTER_CHIPID) == 0x58): # check sensor id 0x58=BMP280
    device.write8(BMP280_REGISTER_SOFTRESET,0xB6) # reset sensor
    time.sleep(0.2) # little break
    device.write8(BMP280_REGISTER_CONTROL,CTRL_MEAS) #
    time.sleep(0.2) # little break
    device.write8(BMP280_REGISTER_CONFIG,CONFIG)  #
    time.sleep(0.2)
    # register_control = device.readU8(BMP280_REGISTER_CONTROL) # check the controll register again
    # register_config = device.readU8(BMP280_REGISTER_CONFIG)# check the controll register again
    # print("config:",register_config)
    # print("control:",register_control)

    dig_T1 = device.readU16LE(BMP280_REGISTER_DIG_T1) # read correction settings
    dig_T2 = device.readS16LE(BMP280_REGISTER_DIG_T2)
    dig_T3 = device.readS16LE(BMP280_REGISTER_DIG_T3)
    dig_P1 = device.readU16LE(BMP280_REGISTER_DIG_P1)
    dig_P2 = device.readS16LE(BMP280_REGISTER_DIG_P2)
    dig_P3 = device.readS16LE(BMP280_REGISTER_DIG_P3)
    dig_P4 = device.readS16LE(BMP280_REGISTER_DIG_P4)
    dig_P5 = device.readS16LE(BMP280_REGISTER_DIG_P5)
    dig_P6 = device.readS16LE(BMP280_REGISTER_DIG_P6)
    dig_P7 = device.readS16LE(BMP280_REGISTER_DIG_P7)
    dig_P8 = device.readS16LE(BMP280_REGISTER_DIG_P8)
    dig_P9 = device.readS16LE(BMP280_REGISTER_DIG_P9)

    #print("dig_T1:",dig_T1," dig_T2:",dig_T2," dig_T3:",dig_T3)
    #print("dig_P1:",dig_P1," dig_P2:",dig_P2," dig_P3:",dig_P3)
    #print(" dig_P4:",dig_P4," dig_P5:",dig_P5," dig_P6:",dig_P6)
    #print(" dig_P7:",dig_P7," dig_P8:",dig_P8," dig_P9:",dig_P9)

    while True: # loop
        raw_temp_msb=device.readU8(BMP280_REGISTER_TEMPDATA_MSB) # read raw temperature msb
        raw_temp_lsb=device.readU8(BMP280_REGISTER_TEMPDATA_LSB) # read raw temperature lsb
        raw_temp_xlsb=device.readU8(BMP280_REGISTER_TEMPDATA_XLSB) # read raw temperature xlsb
        raw_press_msb=device.readU8(BMP280_REGISTER_PRESSDATA_MSB) # read raw pressure msb
        raw_press_lsb=device.readU8(BMP280_REGISTER_PRESSDATA_LSB) # read raw pressure lsb
        raw_press_xlsb=device.readU8(BMP280_REGISTER_PRESSDATA_XLSB) # read raw pressure xlsb

        raw_temp=(raw_temp_msb <<12)+(raw_temp_lsb<<4)+(raw_temp_xlsb>>4) # combine 3 bytes  msb 12 bits left, lsb 4 bits left, xlsb 4 bits right
        raw_press=(raw_press_msb <<12)+(raw_press_lsb <<4)+(raw_press_xlsb >>4) # combine 3 bytes  msb 12 bits left, lsb 4 bits left, xlsb 4 bits right
        # print("raw_press_msb:",raw_press_msb," raw_press_lsb:",raw_press_xlsb," raw_press_xlsb:",raw_press_xlsb)
        # print("raw_temp_msb:",raw_temp_msb,"  raw_temp_lsb:",raw_temp_lsb," raw_temp_xlsb:",raw_temp_xlsb)
        # print("raw_press",raw_press)

        # the following values are from the calculation example in the datasheet
        # this values can be used to check the calculation formulas
        # dig_T1=27504
        # dig_T2=26435
        # dig_T3=-1000
        # dig_P1=36477
        # dig_P2=-10685
        # dig_P3=3024
        # dig_P4=2855
        # dig_P5=140
        # dig_P6=-7
        # dig_P7=15500
        # dig_P8=-14600
        # dig_P9=6000
        # t_fine=128422.2869948
        # raw_temp=519888
        # raw_press=415148

        var1=(raw_temp/16384.0-dig_T1/1024.0)*dig_T2 # formula for temperature from datasheet
        var2=(raw_temp/131072.0-dig_T1/8192.0)*(raw_temp/131072.0-dig_T1/8192.0)*dig_T3 # formula for temperature from datasheet
        temp=(var1+var2)/5120.0 # formula for temperature from datasheet
        t_fine=(var1+var2) # need for pressure calculation

        var1=t_fine/2.0-64000.0 # formula for pressure from datasheet
        var2=var1*var1*dig_P6/32768.0 # formula for pressure from datasheet
        var2=var2+var1*dig_P5*2 # formula for pressure from datasheet
        var2=var2/4.0+dig_P4*65536.0 # formula for pressure from datasheet
        var1=(dig_P3*var1*var1/524288.0+dig_P2*var1)/524288.0 # formula for pressure from datasheet
        var1=(1.0+var1/32768.0)*dig_P1 # formula for pressure from datasheet
        press=1048576.0-raw_press # formula for pressure from datasheet
        press=(press-var2/4096.0)*6250.0/var1 # formula for pressure from datasheet
        var1=dig_P9*press*press/2147483648.0 # formula for pressure from datasheet
        var2=press*dig_P8/32768.0 # formula for pressure from datasheet
        press=press+(var1+var2+dig_P7)/16.0 # formula for pressure from datasheet

        altitude= 44330.0 * (1.0 - pow(press / (QNH*100), (1.0/5.255))) # formula for altitude from airpressure
        print("temperature:{:.2f}".format(temp)+" C  pressure:{:.2f}".format(press/100)+" hPa   altitude:{:.2f}".format(altitude)+" m")
        print("temperature:{:.2f}".format(temp * 1.8 + 32)+" F  pressure:{:.2f}".format(press/100)+" hPa   altitude:{:.2f}".format(altitude*3.2808399)+" ft")
        print

        time.sleep(2)

