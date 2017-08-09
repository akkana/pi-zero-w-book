#!/usr/bin/env python

import twitter
import time

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

def match_keywords(twitapi, topicwords):
    timeline = twitapi.GetHomeTimeline(50)
    matches = {}

    for tweet in timeline:
        text = tweet.text.lower()
        for topic in topicwords:
            for word in topicwords[topic]:
                if word in text:             # Got a match! Add it.
                    if topic in matches:     # saw this topic already
                        matches[topic] += 1
                    else:                    # first time we've seen this topic
                        matches[topic] = 1
    print matches
    return matches

topicwords = {
    'tech':   [ 'raspberry pi', 'linux', 'maker', 'arduino', 'open source'],
    'nature': [ 'bike', 'hike', 'bird', 'bear', 'trail' ]
    }

def match_keywords(twitapi, topicwords):
    timeline = twitapi.GetHomeTimeline(50)

    matches = {}    # Build up a new dictionary of matches to return

    for tweet in timeline:
        text = tweet.text.lower()
        for topic in topicwords:
            for word in topicwords[topic]:
                if word in text:            # Got a match! Add it.
                    if topic in matches:    # saw this topic already
                        matches[topic] += 1
                    else:                   # first time we've seen this topic
                        matches[topic] = 1
    return matches

if __name__ == '__main__':
    twitapi = init_twitter()
    tweets_seen = set()    # The set of tweets already seen

    while True:
        timeline = twitapi.GetHomeTimeline()    # Returns a twitter.Status
        print("\n==========================")
        for tweet in timeline:
            if tweet.id in tweets_seen:
                continue

            print("\n=== %s (%s) ===" % (tweet.user.screen_name,
                                         tweet.user.name))
            print(tweet.text)
            print("    %s" % tweet.created_at)
            tweets_seen.add(tweet.id)

        print("\nTopic words seen:")
        print(match_keywords(twitapi, topicwords))

        time.sleep(120)    # Wait two minutes
