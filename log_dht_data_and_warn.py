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

    rrd_file = cfg.get('settings', 'rrd_file')

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

    #Declare variables
    humidity = None
    temperature = None
    
    while humidity == None and temperature == None:
        humidity, temperature = poll_sensor(cfg)

    rrdtool.update(rrd_file, 'N:{0:0.1f}:{1:0.1f}'.format(temperature, humidity))
    warning_test(humidity, temperature, cfg)

if __name__ == "__main__":
    sys.exit(main())
