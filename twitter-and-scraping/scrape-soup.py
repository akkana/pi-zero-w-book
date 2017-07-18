#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup

def match_keywords(url, topicwords):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")

    # Remove javascript and stylesheets:
    for script in soup(["script", "style"]):
        script.extract()

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
        'tech': [ "linux", "raspberry pi", "arduino", "solder",
                   "open source", "maker" ],
        'science': [ "jupiter", "science", "astronom" ],
        'politics': [ "trump", "gun", "white house", "gop",
                       "democrat", "republican" ],
        }

    #print(match_keywords('http://www.reuters.com/', topicwords))
    print(match_keywords('http://slashdot.org/', topicwords))

