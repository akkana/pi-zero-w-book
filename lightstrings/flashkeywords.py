#!/usr/bin/env python

import twit

import time

# Times in seconds:
TWITTER_CHECK_TIME = 60
TIME_BETWEEN_PIXELS = .02

FLASHFRAC = 10    # How often will we flash?
FLASHTIME = .4
FLASHNUMBER = 2

BLACK = (0, 0, 0)

# NeoPixels or DotStars?
USE_NEOPIXELS = False

if USE_NEOPIXELS:
    # Definitions for NeoPixels:
    from neopixel import Adafruit_NeoPixel, Color, ws

    # LED strip configuration:
    LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).

    # You shouldn't need to change any of these:
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 64     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering
else:
    from dotstar import Adafruit_DotStar, Color

def flash(strip, flashcolor):
    print("Flashing")
    for num in range(FLASHNUMBER):
        for color in (BLACK, flashcolor, BLACK):
            for i in range(num_pixels):
                strip.setPixelColor(i, Color(*color))
            strip.show()
            time.sleep(FLASHTIME)

num_pixels = 30

if USE_NEOPIXELS:
    strip = Adafruit_NeoPixel(num_pixels, LED_PIN,
                              LED_FREQ_HZ, LED_DMA, LED_INVERT,
                              LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
else:
    strip = Adafruit_DotStar(num_pixels, 12000000)

strip.begin()

twitapi = twit.init_twitter()

# For each topic, list some keywords that fit that topic.
# Keywords should be all lower case.
topicwords = {
    'tech':     [ "linux", "raspberry pi", "arduino", "solder",
                  "open source", "maker" ],
    'science':  [ "jupiter", "science", "astronom" ],
    'politics': [ "trump", "gun", "white house", "gop",
                   "democrat", "republican" ],
    'flash':    [ "raspberry pi", "adafruit" ]
    }

topiccolors = {
    'tech':     Color(0, 255,   0),
    'science':  Color(0,   0, 255),
    'politics': Color(255, 0,   0),
    'blank':    Color(0,   0,   0)
    }

flashcolor = (255, 255, 255)

led_number = 0
tot_time = TWITTER_CHECK_TIME
lastflash = 0   # Multiples of FLASHFRAC seconds
while True:
    if tot_time >= TWITTER_CHECK_TIME:
        print("Checking Twitter")
        keywords_found = twit.match_keywords(topicwords)
        tot_time = 0
        print(keywords_found)

    # If the total number of Twitter hits, excluding flashes,
    # divides evenly into the number of pixels, or vice versa,
    # the lights won't advance and that's boring to watch.
    # In that case, add a black pixel.
    tot_hits = sum(keywords_found[i] for i in keywords_found)
    if 'flash' in keywords_found:
        tot_hits -= keywords_found['flash']
    if num_pixels % tot_hits == 0 or tot_hits % num_pixels == 0:
        keywords_found['blank'] = 1

    # Loop over the topics:
    for topic in keywords_found:
        if topic == 'flash':
            totdiv = int(tot_time) / FLASHFRAC
            if totdiv > lastflash:
                lastflash = totdiv
                for i in range(keywords_found[topic]):
                    flash(strip, flashcolor)
                # XXX Add the time we flashed to tot_time
            continue

        # For this topic, keywords_found[topic] is the number of keywords
        # we matched on Twitter. Show that number of pixels.
        # The color for this topic is topiccolors[topic].
        for i in range(keywords_found[topic]):
            strip.setPixelColor(led_number, topiccolors[topic])
            strip.show()

            led_number = (led_number + 1) % num_pixels
            time.sleep(TIME_BETWEEN_PIXELS)
            tot_time += TIME_BETWEEN_PIXELS

