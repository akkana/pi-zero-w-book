#!/usr/bin/env python

import RPi.GPIO as GPIO
import smbus

import twit

import sys
import os
import time, calendar

MCP9808_address = 0x18         # The default I2C address of the MCP9808
MCP9808_temp_reg = 0x05
bus = smbus.SMBus(1)

def read_temperature_c():
    '''Read and teturn the current temperature in Celsius'''

    data = bus.read_i2c_block_data(MCP9808_address, MCP9808_temp_reg)

    # Calculate temperature (see 5.1.3.1 in the datasheet,
    # though it's a little confusing and seems to conflate 32C and 0C):
    ctemp = (((data[0] & 0x0f) << 8) + data[1]) / 16.0
    if data[0] & 0x10:
        ctemp = 256 - ctemp
    return ctemp

messages_seen = set()

def check_for_command(twitapi, code, recentminutes):
    '''Check for the most recent direct message that starts with code
       and was sent in the specified number of minutes.
       Look for the command after the code, so for example, AC ON.
       Returns (cmd, user) if there was a command,
       where command is a string like "ON" and user is a screen name.
       Returns (None, None) if there was no command.
    '''
    DMs = twitapi.GetDirectMessages(count=5, skip_status=True)
    now = time.time()
    for msg in DMs:
        # Have we already seen this message?
        if msg.id in messages_seen:
            break
        messages_seen.add(msg.id)

        if msg.text.startswith(code):
            # strip off the code part to get the ON or OFF command:
            cmd = msg.text[len(code):].strip()

            # Parse the creation time for the message,
            # make sure it was sent recently
            t = time.strptime(msg.created_at,
                              '%a %b %d %H:%M:%S +0000 %Y')
            # How old is the message?
            minutesold = (now - calendar.timegm(t)) / 60
            if minutesold > recentminutes:
                break

            # We have a valid command.
            return cmd, msg.sender_screen_name

    # Didn't see a command:
    return None, None

if __name__ == '__main__':
    twitapi = twit.init_twitter()

    powerswitch = 14       # GPIO pin for the Powerswitch Tail
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(powerswitch, GPIO.OUT)

    while True:
        ctemp = read_temperature_c()
        ftemp = ctemp * 1.8 + 32

        # How to post the temperature to Twitter.
        # This can fail for several reasons: for instance,
        # if we try to tweet the same temperature twice in a row,
        # we'll get code 187, 'Status is a duplicate.'.
        # Guard against that.
        try:
            if ftemp > 90:
                twitapi.PostUpdate("It's too hot! %.1f degrees!" % ftemp)
        except twitter.TwitterError as e:
            print("Twitter error: %s" % str(e))

        cmd, user = check_for_command(twitapi, "FAN", 30)
        if cmd == "ON":
            GPIO.output(powerswitch, GPIO.HIGH)
            twitapi.PostDirectMessage("Turned fan ON", screen_name=user)
        elif cmd == "OFF":
            GPIO.output(powerswitch, GPIO.LOW)
            twitapi.PostDirectMessage("Turned fan OFF", screen_name=user)
        elif cmd:
            twitapi.PostDirectMessage("I don't understand command %s" % cmd,
                                      screen_name=user)

        time.sleep(60 * 5)   # sleep 5 minutes between checks
