#!/usr/bin/env python

import requests

def match_keywords(url, topicwords):
    r = requests.get(url)

    matches = {}

    for line in r.text.splitlines():
        line = line.lower()    # convert it to lowercase
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
        'tech':   [ 'raspberry pi', 'linux', 'maker', 'arduino', 'open source', 'security', 'privacy', 'gimp' ],
        'nature': [ 'bike', 'hike', 'bird', 'bear', 'trail', 'school', 'moon', 'bird' ]
    }

    print(match_keywords('http://slashdot.org', topicwords))
