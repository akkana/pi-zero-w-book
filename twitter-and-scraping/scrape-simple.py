#!/usr/bin/env python

import requests

def match_keywords(url, topicwords):
    print("Fetching " + url + " ...")
    r = requests.get(url)

    matches = {}

    for line in r.text.splitlines():
        for topic in topicwords:
            for word in topicwords[topic]:
                if word in line:
                    # Add it to matches
                    if topic in matches:
                        matches[topic] += 1
                    else:
                        matches[topic] = 1
    return matches


if __name__ == '__main__':
    topicwords = {
        'scitech': [ "tesla", "disease", "environment", "self-driving" ],
        'politics': [ "trump", "gun", "white house", "gop",
                       "democrat", "republican" ],
        }

    print(match_keywords('http://www.reuters.com/', topicwords))

