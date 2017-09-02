#!/usr/bin/env python

import twitter
import os

tweets_seen = set()

def init_twitter():
    '''Authenticate and return a twitter.Api object'''

    conffile = os.path.expanduser("~/.config/YOUR_APP_NAME/auth")
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

def print_timeline(api):
    timeline = api.GetHomeTimeline()    # Returns twitter.Status[]
    print("\n==========================")
    for tweet in timeline:
        if tweet.id in tweets_seen:
            continue

        print("\n=== %s (%s) ===" % (tweet.user.screen_name,
                                     tweet.user.name))
        print(tweet.text)
        print("\n    %s" % tweet.created_at)
        tweets_seen.add(tweet.id)

def match_keywords(twitapi, topicwords):
    timeline = twitapi.GetHomeTimeline(50)    # Returns twitter.Status[]

    matches = {}

    for tweet in timeline:
        text = tweet.text.lower()
        # print text
        # print
        for topic in topicwords:
            for word in topicwords[topic]:
                if word in text:
                    # Add it to matches
                    if topic in matches:
                        matches[topic] += 1
                    else:
                        matches[topic] = 1
    return matches

if __name__ == '__main__':
    import time

    twitapi = init_twitter()

    # For each mood, list some keywords that fit that mood.
    # Keywords should be all lower case.
    topicwords = {
        'tech':     [ "linux", "raspberry pi", "arduino", "solder",
                       "open source", "maker" ],
        'science':  [ "jupiter", "science", "astronom" ],
        'politics': [ "trump", "gun", "white house", "gop",
                       "democrat", "republican" ],
        }

    while True:
        print_timeline(twitapi)
        print()
        print(match_keywords(twitapi, topicwords))
        time.sleep(30)

