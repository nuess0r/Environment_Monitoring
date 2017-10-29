#!/usr/bin/python
# Author: Christoph Zimmermann
# Based on Code from Tony DiCola (Copyright (c) 2014 Adafruit Industries)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import os
import time
import Adafruit_DHT
from datetime import datetime
from smbus import SMBus
from PIL import ImageFont, ImageDraw, Image

from OLED_SSD1306_128x64.oled import ssd1306

# Define type and pin of connected humidity sensor
dht_type      = 22
dht_pin       = 4

# Define true type font to use
dirname = os.path.dirname(__file__)
font_file = os.path.join(dirname, 'OLED_SSD1306_128x64', 'resources/FreeSans.ttf')

# Setup display
i2cbus = SMBus(1)        # 1 = Raspberry Pi but NOT early REV1 board
display = ssd1306(i2cbus)   # create oled object, nominating the correct I2C bus, default address

# "draw" onto this canvas, then call flush() to send the canvas contents to the hardware.
canvas = display.canvas

# Put border around the screen:
display.canvas.rectangle((0, 0, display.width-1, display.height-1), outline=1, fill=0)

# Write welcome message to display
font = ImageFont.truetype(font_file, 16)
canvas.text((6, 6), 'Data Logger for', font=font, fill=1)
canvas.text((6, 24), 'Temperature', font=font, fill=1)
canvas.text((6, 41), 'and Humidity', font=font, fill=1)
display.flush()
time.sleep(5)

# Load smaller font for the data display
font = ImageFont.truetype(font_file, 13)

while(True):
    # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(dht_type, dht_pin)

    # Note that sometimes you won't get a reading and
    # the results will be null (because Linux can't
    # guarantee the timing of calls to read the sensor).
    # If this happens try again!
    if humidity is not None and temperature is not None:
        #print('Temp={0:0.1f}C  Humidity={1:0.1f}%'.format(temperature, humidity))
        dt = datetime.now()
        display.canvas.rectangle((0, 0, display.width-1, display.height-1), outline=0, fill=0)
        canvas.text((6, 4), dt.strftime("%d. %B %Y %H:%M"), font=font, fill=1)
        canvas.text((6, 30), 'Temperature {0:0.1f}C'.format(temperature), font=font, fill=1)
        canvas.text((6, 46), 'Humidity {0:0.1f}%'.format(humidity), font=font, fill=1)
        display.flush()
    time.sleep(5)
