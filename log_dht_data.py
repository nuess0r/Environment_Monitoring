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
import os.path
import rrdtool

import Adafruit_DHT

# Define type and pin of connected humidity sensor
dht_type      = 11
dht_pin       = 4

# Define the path and file name for the rrd database
rrd_file      = '/home/pi/temp_humidity.rrd'

if not os.path.isfile(rrd_file):
    rrdtool.create(rrd_file,
         '--step', '300',
         'DS:temperature:GAUGE:600:-270:200',
         'DS:humidity:GAUGE:600:0:100',
         'RRA:AVERAGE:0.5:2:144',
         'RRA:AVERAGE:0.5:12:24',
         'RRA:AVERAGE:0.5:288:31',
         'RRA:AVERAGE:0.5:2016:52',
         'RRA:MAX:0.5:2:144',
         'RRA:MAX:0.5:12:24',
         'RRA:MAX:0.5:288:31',
         'RRA:MAX:0.5:2016:52',
         'RRA:MIN:0.5:2:144',
         'RRA:MIN:0.5:12:24',
         'RRA:MIN:0.5:288:31',
         'RRA:MIN:0.5:2016:52')

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(dht_type, dht_pin)

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!

if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}C  Humidity={1:0.1f}%'.format(temperature, humidity))
    print('N:{0:0.1f}:{1:0.1f}'.format(temperature, humidity))
    rrdtool.update(rrd_file, 'N:{0:0.1f}:{1:0.1f}'.format(temperature, humidity))
