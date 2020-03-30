#!/usr/bin/env python
# encoding: utf-8
#
# Copyright 2017 Christoph Zimmermann
#
# This file is based on the raspberry_preserve project from Daniel Fairchild
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import sys
import time
import os
import ConfigParser
import socket
import fcntl
import struct
import smtplib
import rrdtool
import Adafruit_DHT
from datetime import datetime
from smbus import SMBus
from PIL import ImageFont, ImageDraw, Image

from OLED_SSD1306_128x64.oled import ssd1306


def read_config(fname):

    #read config file if present
    cfg = ConfigParser.ConfigParser(allow_no_value=True)
    if os.path.exists(fname):
        cfg.read(fname)
    else:
        print('Config file ' + fname + ' not found')

    if not cfg.has_section("settings"):
        print('Config file has no section settings. Consult the example config')

    return cfg

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def poll_sensor(cfg):
    # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    sensor = int(cfg.get('settings', 'sensor_type'))
    pin = int(cfg.get('settings', 'sensor_pin'))
    return Adafruit_DHT.read_retry(sensor, pin)

def send_warning(descr, value, cfg, toaddrs=None):
    # Specifying the from and to addresses
    from_address = cfg.get('settings', 'alarm_from_address');
    if toaddrs == None:
        toaddrs  = cfg.get('settings', 'alarm_to_addresses');
    node_name = cfg.get('settings', 'node_name');
    node_description = cfg.get('settings', 'node_description');
    node_netaddress =  cfg.get('settings', 'node_netaddress');

    if node_netaddress == '':
        node_netaddress = get_ip_address('eth0')

    header = """From: %s
To: %s
Subject: %s warning from %s


"""  % (from_address, toaddrs, descr, node_name)
    message = """
%s of %.2f measured on %s.

%s has the following description: %s

Browse the data history of %s at:
%s .

""" %(descr, float(value), node_name,
    node_name, node_description,
    node_name, node_netaddress)

    # SMTP server login
    username = cfg.get('settings', 'smtp_username');
    password = cfg.get('settings', 'smtp_password');

    # Sending the mail
    server = smtplib.SMTP(cfg.get('settings', 'smtp_server'))
    server.starttls()

    if len(username) > 0 and len(password) > 0:
        server.login(username,password)
    server.sendmail(from_address, toaddrs.split(";"), header + message)
    server.quit()

def warning_test(humidity, temperature, cfg):
    #if humidity outside range
    if humidity < float(cfg.get('settings', 'humidity_min')):
        send_warning("Low humidty", humidity, cfg)
    if humidity > float(cfg.get('settings', 'humidity_max')):
        send_warning("High humidty", humidity, cfg)

    if temperature > float(cfg.get('settings', 'temperature_max')):
        send_warning("High temperature", temperature, cfg)

def main(argv=None):
    dirname = os.path.dirname(__file__)
    config_file = os.path.join(dirname, 'log_dht_data_and_warn.cfg')
    cfg = read_config(config_file)

    # Define true type font to use
    font_file = os.path.join(dirname, 'OLED_SSD1306_128x64', 'resources/FreeSans.ttf')

    # Setup display
    i2cbus = SMBus(1)           # 1 = Raspberry Pi but NOT early REV1 board
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



    rrd_file = cfg.get('settings', 'rrd_file')

    if not os.path.isfile(rrd_file):
        # create a round-robin database that expects every 5 s a value
        # it creates max/min/average values for:
        # * 10 min
        # * 1 h
        # * 24 h
        # * 7 days
	rrdtool.create(rrd_file,
                       '--step', '5',
		       'DS:temperature:GAUGE:60:-270:200',
		       'DS:humidity:GAUGE:60:0:100',
                       'RRA:AVERAGE:0.5:120:288',
		       'RRA:AVERAGE:0.5:720:48',
		       'RRA:AVERAGE:0.5:17280:62',
		       'RRA:AVERAGE:0.5:120960:104',
                       'RRA:MAX:0.5:120:288',
		       'RRA:MAX:0.5:720:48',
		       'RRA:MAX:0.5:17280:62',
		       'RRA:MAX:0.5:120960:104',
                       'RRA:MIN:0.5:120:288',
                       'RRA:MIN:0.5:720:48',
                       'RRA:MIN:0.5:17280:62',
                       'RRA:MIN:0.5:120960:104')


    while(True):
        humidity = None
        temperature = None

        while humidity == None and temperature == None:
            humidity, temperature = poll_sensor(cfg)

        rrdtool.update(rrd_file, 'N:{0:0.1f}:{1:0.1f}'.format(temperature, humidity))

        warning_test(humidity, temperature, cfg)

        dt = datetime.now()
        display.canvas.rectangle((0, 0, display.width-1, display.height-1), outline=0, fill=0)
        canvas.text((6, 4), dt.strftime("%d. %B %Y %H:%M"), font=font, fill=1)
        # Note that sometimes you won't get a reading and
        # the results will be null (because Linux can't
        # guarantee the timing of calls to read the sensor).
        # If this happens try again!
        if humidity is not None and temperature is not None:
            #print('Temp={0:0.1f}C  Humidity={1:0.1f}%'.format(temperature, humidity))
            canvas.text((6, 30), 'Temperature {0:0.1f}C'.format(temperature), font=font, fill=1)
            canvas.text((6, 46), 'Humidity {0:0.1f}%'.format(humidity), font=font, fill=1)
        display.flush()

        time.sleep(5)

if __name__ == "__main__":
    sys.exit(main())
