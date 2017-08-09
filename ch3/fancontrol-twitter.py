#!/usr/bin/env python

import twitter
import calendar
import time
import RPi.GPIO as GPIO

def init_twitter():
    conffile = "/home/pi/.config/YOUR_APP_NAME/auth"
    oauthtokens = {}
    with open(conffile) as conf:
        for line in conf:
            line = line.split()
            oauthtokens[line[0]] = line[1]

    return twitter.Api(
        consumer_key=oauthtokens["consumer"],
        consumer_secret=oauthtokens["consumer_secret"],
        access_token_key=oauthtokens["access_token"],
        access_token_secret=oauthtokens["access_token_secret"])

twitapi = init_twitter()
messages_seen = set()

def check_for_command(twitapi, code, recentminutes):
    '''Check for the most recent direct message that
       starts with code and was sent in the specified
       number of minutes.
       Look for the command after the code, e.g. FAN ON.
       Returns (cmd, user) if there was a command,
       where command is a string like "ON"
       and user is a screen name.
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
            # strip off the code part to get the ON/OFF command:
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
    twitapi = init_twitter()

    powerswitch = 14
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(powerswitch, GPIO.OUT)

    try:
        while True:
            cmd, user = check_for_command(twitapi, "FAN", 30)
            if cmd == "ON":
                print("Turning fan on")
                GPIO.output(powerswitch, GPIO.HIGH)
                twitapi.PostDirectMessage("Turned fan ON",
                                          screen_name=user)
            elif cmd == "OFF":
                print("Turning fan off")
                GPIO.output(powerswitch, GPIO.LOW)
                twitapi.PostDirectMessage("Turned fan OFF",
                                          screen_name=user)
            elif cmd:
                twitapi.PostDirectMessage("Unknown cmd %s"
                                          % cmd,
                                          screen_name=user)
            else:
                print("Didn't see a command")

            print("Sleeping")
            time.sleep(60 * 5)   # sleep 5 minutes between checks

    except KeyboardInterrupt:
        print("Cleaning up")
        GPIO.cleanup()
