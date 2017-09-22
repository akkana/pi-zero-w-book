#!/usr/bin/env python

# Draw a little calendar on a 128x64 OLED display using Adafruit's library.

# https://learn.adafruit.com/ssd1306-oled-displays-with-raspberry-pi-and-beaglebone-black/overview

# To use this display on Arduino, see
# https://github.com/adafruit/Adafruit_SSD1306

import calendar, datetime, time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

import Image
import ImageDraw
import ImageFont

import sys, os

# Raspberry Pi pin configuration:
# VCC->3.3V, Gnd->Gnd, SCL->SCL (GPIO 3), SDA->SDA (GPIO 2).
# There's no reset pin, so make up a number since the Adafruit lib requires one:
RST = 24

# Inspired by the calendar shown in
# https://www.eevblog.com/forum/projects/tiny-oled-128x64-calendar-display-(arduino)/
# but that code looks way complex, so here's a simple Python version.
def draw_calendar(disp, year, month):
    '''Draw a calendar for the given month and year
        (will default to the current month/year).
    '''

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Load default font.
    font = ImageFont.load_default()

    # Geometry for printing the calendar.
    padding = 1
    lineheight = (height - padding*2) / 6  # XXX can be 5 or 7in some months
    colwidth = (width - padding*2) / 7
    y = padding

    highlight_cur = year == now.year and month == now.month

    calendar.setfirstweekday(calendar.SUNDAY)

    # Header:
    daysheader = [ "Su", "Mo", "Tu", "We", "Th", "Fr", "Sa" ]
    x = padding
    for dh in daysheader:
        draw.text((x, y), dh, font=font, fill=255)
        x += colwidth
    y += lineheight

    # If you don't need to highlight the current day, use
    # calendar.TextCalendar(calendar.SUNDAY).formatmonth(year, month)
    # But we do, so:
    monthcal = calendar.monthcalendar(year, month)
    for row in monthcal:
        x = padding
        for day in row:
            daystr = "%2d" % day if day else "  "

            if highlight_cur and day == now.day:
                draw.rectangle((x-padding*2, y-padding,
                                x+colwidth-padding*5, y+lineheight+padding),
                               outline=255, fill=255)
                draw.text((x, y), daystr, font=font, fill=0)
            else:
                draw.text((x, y), daystr, font=font, fill=255)

            x += colwidth

        y += lineheight

    # Display image.
    disp.image(image)
    disp.display()

# draw_shapes is from Adafruit's example,
# https://learn.adafruit.com/ssd1306-oled-displays-with-raspberry-pi-and-beaglebone-black?view=all
# It isn't used in drawing the calendar, and is just included here
# for useful examples of how to draw shapes.
def draw_shapes(disp):
    # Initialize library.
    disp.begin()

    # Clear display.
    disp.clear()
    disp.display()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = 2
    shape_width = 20
    top = padding
    bottom = height-padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = padding
    # Draw an ellipse.
    draw.ellipse((x, top , x+shape_width, bottom), outline=255, fill=0)
    x += shape_width+padding
    # Draw a rectangle.
    draw.rectangle((x, top, x+shape_width, bottom), outline=255, fill=0)
    x += shape_width+padding
    # Draw a triangle.
    draw.polygon([(x, bottom), (x+shape_width/2, top), (x+shape_width, bottom)], outline=255, fill=0)
    x += shape_width+padding
    # Draw an X.
    draw.line((x, bottom, x+shape_width, top), fill=255)
    draw.line((x, top, x+shape_width, bottom), fill=255)
    x += shape_width+padding

    # Load default font.
    font = ImageFont.load_default()

    # Alternatively load a TTF font.
    # Some other nice fonts to try: http://www.dafont.com/bitmap.php
    #font = ImageFont.truetype('Minecraftia.ttf', 8)

    # Write two lines of text.
    draw.text((x, top),    'Hello',  font=font, fill=255)
    draw.text((x, top+15), 'World!', font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()

if __name__ == '__main__':

    def Usage():
        print("Usage: %s [year] [month]" % os.path.basename(sys.argv[0]))
        sys.exit(1)

    # parse arguments
    now = datetime.datetime.now()
    month = now.month
    year = now.year
    for arg in sys.argv[1:]:
        try:
            n = int(arg)
        except ValueError:
            print("Don't understand " + arg)
            Usage()
        if n > 31:
            year = n
        else:
            month = n

    # 128x64 display with hardware I2C:
    disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

    draw_shapes(disp)
    time.sleep(5)
    draw_calendar(disp, year, month)


