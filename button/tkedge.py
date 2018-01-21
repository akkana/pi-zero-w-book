#!/usr/bin/env python

import Tkinter

from RPi import GPIO
import time

class ButtonWindow:
    def __init__(self, button_pin):
        self.button_pin = button_pin

        self.tkroot = Tkinter.Tk()
        self.tkroot.geometry("100x60")

        self.label = Tkinter.Label(self.tkroot, text="????",
                                   bg="black", fg="white")
        self.label.pack(padx=5, pady=10, side=Tkinter.LEFT)

        self.set_up_GPIO()

    def set_up_GPIO(self):
        GPIO.setmode(GPIO.BCM)

        # Wire the button to +3.3, then enable an internal pulldown.
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # events can be GPIO.RISING, GPIO.FALLING, or GPIO.BOTH
        GPIO.add_event_detect(self.button_pin, GPIO.BOTH,
                              callback=self.button_handler,
                              bouncetime=300)

    def mainloop(self):
        self.tkroot.mainloop()

    def button_handler(self, channel):
        time.sleep(.01)
        if GPIO.input(channel):
            self.label.config(text="ON")
            self.label.configure(bg="red")
        else:
            self.label.config(text="OFF")
            self.label.configure(bg="blue")

if __name__ == '__main__':
    win = ButtonWindow(18)

    win.mainloop()

