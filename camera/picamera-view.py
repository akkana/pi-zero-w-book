#!/usr/bin/env python

# start: https://www.raspberrypi.org/documentation/usage/camera/python/README.md
# Full doc: http://picamera.readthedocs.io/en/release-1.13/
# Useful recipes: http://picamera.readthedocs.io/en/release-1.10/recipes1.html

# requires: python-picamera python-imaging-tk

import io
import time
import sys
import picamera
import Tkinter
from PIL import Image, ImageTk

root = Tkinter.Tk()

def quit(event):
    sys.exit(0)

root.bind("q", quit)
root.bind("ctrl+q", quit)

# Create the in-memory stream to capture the image:
stream = io.BytesIO()
with picamera.PiCamera() as camera:
    camera.start_preview()
    time.sleep(.5)
    camera.capture(stream, format='jpeg')

# "Rewind" the stream to the beginning so we can read its content
stream.seek(0)
image = Image.open(stream)

# Now show it in the Tk window.
photoimage = ImageTk.PhotoImage(image)
label = Tkinter.Label(root, image=photoimage)
label.pack()

root.mainloop()

