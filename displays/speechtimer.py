#!/usr/bin/env python

# This uses https://luma-led-matrix.readthedocs.io/

# Wiring:
# MAX7219	Name 	Remarks 	RPi Pin	RPi Function
# 1 	VCC 	+5V Power 	2 	5V0
# 2 	GND 	Ground 		6 	GND
# 3 	DIN 	Data In 	19 	GPIO 10 (MOSI)   via level shifter
# 4 	CS 	Chip Select 	24 	GPIO 8 (SPI CE0) via level shifter
# 5 	CLK 	Clock 	23 	GPIO 11 (SPI CLK)        via level shifter
# A bidirectional logic level shifter works.

from __future__ import print_function

import time
import sched

import RPi.GPIO as GPIO

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import sevensegment

# Button class to keep track of things like longpress and debouncing.
class Button:
    debouncetime = 1
    longpresstime = 2

    def __init__(self, pin):
        self.pin = pin
        self.last_press = 0
        self.last_release = 0

        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def check_press(self, now):
        '''Returns 0 (off), 1 (on), 2 (longpress)
           Will return 1 only once for each press.
           Normal presses are returned only after the rlease,
           but longpresses are returned as soon as we know it's a longpress,
           and we'll keep returning longpresses until it's released.
           Pass in time so we don't have to call time.time() for every button.
        '''
        # Need to invert the input since we're using internal pullups:
        state = not GPIO.input(self.pin)

        if self.last_press > self.last_release:
            # The button was already pressed the last time we were called.
            if state:    # It's still pressed.
                # Is it a longpress?
                if now - self.last_press > Button.longpresstime:
                    return 2
                return 0

            # Otherwise it's recently been released. Check the time
            # and return either a press or a longpress
            self.last_release = now
            # If we've been longpressing, return 0 now.
            if now - self.last_press > Button.longpresstime:
                return 0
            # else return the press.
            return 1

        # Else the button wasn't previously pressed. Is it now?
        if state:    # newly pressed
            self.last_press = now
            # Don't return a press yet: we don't know whether it's
            # a normal press or a longpress until the release.
            return 0

        return 0

class SpeechTimer:
    def __init__(self, seg, minutes, startstoppin, updownpins, lightpins):
        '''
        seg: the max7219 8-segment display.
        startstoppin: Pin for the start/stop button (use internal pullup)
        updownpins: Two pins, for up and down (internal pullup).
        lightpins: Three pins, for green, yellow, red.
        '''
        self.seg = seg
        self.lightpins = lightpins

        self.startbutton = Button(startstoppin)
        self.upbutton = Button(updownpins[0])
        self.downbutton = Button(updownpins[1])

        # Goal minutes:
        self.goalmin = minutes

        # start time and goal time, both in seconds.
        # If they're None, the timer isn't currently running.
        self.goaltime = None
        self.starttime = None

        # Elapsed time if the timer has been started, else None.
        # If elapsed and not starttime, the timer is paused.
        self.elapsed = None

        # scheduler will be set in run()
        self.scheduler = None

        # Enable the three LEDs:
        for pin in self.lightpins:
            GPIO.setup(pin, GPIO.OUT)

        # Finally, start the scheduler.
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.tick()
        self.scheduler.run()

    def tick(self):
        '''tick is called a few times per second, whether or not we're timing.
           It updates the display, checks the buttons and acts accordingly,
           then reschedules itself for the next second.
        '''
        now = time.time()

        # Check the various button states.

        # Is the start button pressed? Check for longpress too.
        startpressed = self.startbutton.check_press(now)
        if startpressed > 1:
            if not self.starttime:
                self.starttime = None
                self.goaltime = None
                self.elapsed = None

        elif startpressed:
            # Is the clock stopped? Start it.
            if not self.elapsed:
                self.starttime = now
                self.goaltime = self.starttime + self.goalmin * 60
                self.elapsed = 0
            # Is the clock running? Pause it.
            elif self.starttime:
                self.elapsed = now - self.starttime
                self.starttime = None
                self.goaltime = None

            # else the clock is paused; restart it.
            else:
                self.starttime = now - self.elapsed
                self.goaltime = self.starttime + self.goalmin * 60

        if self.upbutton.check_press(now):
            self.goalmin += 1

        elif self.downbutton.check_press(now):
            self.goalmin -= 1
            if self.goalmin < 1:
                self.goalmin = 1

        if self.starttime:    # clock is running
            self.elapsed = int(now - self.starttime)
            minutes = int(self.elapsed / 60)
            seconds = int(self.elapsed % 60)
            # print("%02d:%02d" % (minutes, seconds))
            seg.text = "%-4d%02d.%02d" % (self.goalmin, minutes, seconds)

        elif self.elapsed:    # Started but paused
            minutes = int(self.elapsed / 60)
            seconds = int(self.elapsed % 60)
            seg.text = "%-4d.%02d.%02d" % (self.goalmin, minutes, seconds)
            # Flash when we're paused
            # if self.elapsed % 2:
            #     seg.text = "%-4d%02d.%02d" % (self.goalmin, minutes, seconds)
            # else:
            #     seg.text = "%-4d    " % (self.goalmin)

        else:
            seg.text = "%-4d    " % (self.goalmin)

        self.gyr(now)

        # The next time we'll tick. Make it far enough ahead that
        # we won't miss it.
        nexttime = time.time() + .3
        self.scheduler.enterabs(nexttime, 1, self.tick, ())

    def set_lights(self, green, yellow, red):
        for i, val in enumerate((green, yellow, red)):
            GPIO.output(self.lightpins[i], GPIO.HIGH if val else GPIO.LOW)

    def gyr(self, curtime):
        '''Set the green, yellow, red lights
           depending on the current time and goal time.
        '''
        if not self.goaltime:
            # If starttime is set but goaltime isn't,
            # we've started the timer but temporarily stopped it.
            # Whatever the lights are now, don't change them.
            if self.elapsed:
                return
            # If neither goaltime nor starttime are set, we're not running.
            # Lights should all be off.
            return self.set_lights(False, False, False)

        # No matter how long the speech, if we're over the goal time
        # by more than half a minute, the red light should flash, so
        # it will be True on odd seconds, False on even seconds.
        if curtime > self.goaltime + 30:
            print("flashing red")
            return self.set_lights(False, False,
                                   (True if (int(curtime) % 2) else False))

        # If we're over time but not by more than half a minute, light the red:
        if curtime > self.goaltime:
            return self.set_lights(False, False, True)

        # For times 15 minutes and up, green and yellow get 2.5 minutes each.
        if self.goalmin >= 15:
            if curtime > self.goaltime - 150:    # yellow
                return self.set_lights(False, True, False)
            if curtime > self.goaltime - 300:      # green
                return self.set_lights(True, False, False)
            return False, False, False

        # For times 4 minutes and up, green and yellow get 1 minute each.
        if self.goalmin >= 4:
            if curtime > self.goaltime - 60:    # yellow
                return self.set_lights(False, True, False)
            if curtime > self.goaltime - 120:   # green
                return self.set_lights(True, False, False)
            return self.set_lights(False, False, False)

        # Under 4 minutes, each light only gets 30 seconds
        if curtime > self.goaltime - 30:    # yellow
            return self.set_lights(False, True, False)
        if curtime > self.goaltime - 60:    # green
            return self.set_lights(True, False, False)
        return self.set_lights(False, False, False)

if __name__ == '__main__':
    try:
        # create seven segment device
        serial = spi(port=0, device=0, gpio=noop())
        device = max7219(serial, cascaded=1)
        seg = sevensegment(device)

        GPIO.setmode(GPIO.BCM)
        timer = SpeechTimer(seg, minutes=2,
                            startstoppin=13, updownpins=(5, 6),
                            lightpins=(17, 27, 22))

    except KeyboardInterrupt:
        print("Interrupt")

    finally:
        print("Cleaning up")
        GPIO.cleanup()

