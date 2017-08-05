#!/usr/bin/env python

import twit

# Define this to NeoPixel or DotStar
type = "NeoPixel"

# Set up whichever type of strip we're using:
if type = "DotStar"
    # For DotStars:
    from dotstar import Adafruit_DotStar, Color
    num_pixels = 30
    strip = Adafruit_DotStar(num_pixels, 12000000)
    strip.begin()

else:
    # For NeoPixels:
    from neopixel import Adafruit_NeoPixel, Color, ws

    # LED strip configuration:
    LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 256     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering
    [AU: is this part of program or can we change to color? LW]

    num_pixels = 7

    strip = Adafruit_NeoPixel(num_pixels, LED_PIN,
                              LED_FREQ_HZ, LED_DMA, LED_INVERT,
                              LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)

# Initialize the strip, whichever type it is:
strip.begin()

# Following topics:
topicwords = {
    'tech':   [ 'raspberry pi', 'linux', 'maker', 'arduino', 'open source'],
    'nature': [ 'bike', 'hike', 'bird', 'bear', 'trail' ]
    }

def match_keywords(twitapi, topicwords):
    timeline = twitapi.GetHomeTimeline(50)
    matches = {}

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

topiccolors = {
    'nature': Color(  0, 255,   0),
    'tech':   Color(255,   0, 255),
    }

TWITTER_CHECK_TIME = 120       # How often to check Twitter
TIME_BETWEEN_PIXELS = .02      # Seconds from one pixel to the next
led_number = 0                 # Which LED are we setting right now?
tot_time = TWITTER_CHECK_TIME  # So we'll check immediately

while True:
    if tot_time >= TWITTER_CHECK_TIME:
        keywords_found = twit.match_keywords(topicwords)
        tot_time = 0
        print(keywords_found)

    # If the total number of Twitter hits, excluding flashes,
    # divides evenly into the number of pixels, or vice versa,
    # the lights won't advance and that's boring to watch.
    # In that case, add a black pixel.
    tot_hits = sum(keywords_found[i] for i in keywords_found)
    if num_pixels % tot_hits == 0 or tot_hits % num_pixels == 0:
        keywords_found['blank'] = 1

    # Loop over the topics:
    for topic in keywords_found:
        # For this topic, keywords_found[topic] is the number of keywords
        # we matched on Twitter. Show that number of pixels.
        # The color for this topic is topiccolors[topic].
        for i in range(keywords_found[topic]):
            strip.setPixelColor(led_number, topiccolors[topic])
            strip.show()

            led_number = (led_number + 1) % num_pixels
            time.sleep(TIME_BETWEEN_PIXELS)
            tot_time += TIME_BETWEEN_PIXELS


