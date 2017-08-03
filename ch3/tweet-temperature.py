#!/usr/bin/env python

import twitter
import MCP9808

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

twitapi = twit.init_twitter()

while True:
    ctemp = MCP9808.read_temperature_c()
    ftemp = ctemp * 1.8 + 32
    try:
        if ftemp > 90:
            twit.PostUpdate("Whew, it's too hot, %.1f degrees!" % ftemp)
        else:
            twit.PostUpdate("The temperature is %.1f degrees." % ftemp)
    except twitter.TwitterError as e:
        print("Twitter error: %s" % str(e))
