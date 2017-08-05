#!/usr/bin/env python

import twitter
import time

def init_twitter():
    conffile = "/home/pi/.config/YOUR_APP_NAME/auth"
    conffile = "/home/akkana/.config/scrubjay/auth"
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

if __name__ == '__main__':
    twitapi = init_twitter()

    tweets_seen = set()

    while True:
        timeline = twitapi.GetHomeTimeline()    # Returns a twitter.Status
        print("==========================")
        for tweet in timeline:
            if tweet.id in tweets_seen:
                continue

            print()
            print("=== %s (%s) ===" % (tweet.user.screen_name,
                                       tweet.user.name))
            print(tweet.text)
            print("    %s" % tweet.created_at)
            tweets_seen.add(tweet.id)
        time.sleep(120)    # Wait two minutes
