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
import time

import Adafruit_GPIO.PCF8574 as PCF
from Adafruit_CharLCD import Adafruit_CharLCD
import Adafruit_DHT

# Define type and pin of connected humidity sensor
dht_type      = 11
dht_pin       = 4

# Define PCF pins connected to the LCD.
lcd_rs        = 0
lcd_rw        = 1
lcd_en        = 2
lcd_backlight = 3
d4,d5,d6,d7   = 4,5,6,7
cols,lines    = 16,2

gpio = PCF.PCF8574(address=0x3f)

gpio.setup(lcd_rw, PCF.OUT)
gpio.output(lcd_rw, 0)

# Instantiate LCD Display
lcd = Adafruit_CharLCD(lcd_rs, lcd_en, d4, d5, d6, d7, cols, lines, 
                       lcd_backlight, invert_polarity=False, gpio=gpio)

lcd.clear()
lcd.message('Humidity and\nTemperature')
lcd.set_backlight(1)

while(True):
    # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(dht_type, dht_pin)

    # Note that sometimes you won't get a reading and
    # the results will be null (because Linux can't
    # guarantee the timing of calls to read the sensor).
    # If this happens try again!
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}C  Humidity={1:0.1f}%'.format(temperature, humidity))
        lcd.clear()
        lcd.message('Temp={0:0.1f}C\nHumidity={1:0.1f}%'.format(temperature, humidity))
    time.sleep(5)
