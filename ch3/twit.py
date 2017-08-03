#!/usr/bin/env python

import twitter

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

