#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup

def match_keywords(url, topicwords):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")

    # Remove javascript:
    for script in soup(["script"]):
        script.extract()      # Remove all <script> tags

    matches = {}

    for line in soup.text.lower().splitlines():
        for topic in topicwords:
            for word in topicwords[topic]:
                if word in line:
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
