#!/usr/bin/env python
# Author: Christoph Zimmermann

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
import socket
import fcntl
import struct
from PIL import ImageFont, ImageDraw, Image

from OLED_SSD1306_128x64.oled import ssd1306
from smbus import SMBus

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def main(argv=None):
    dirname = os.path.dirname(__file__)
    font_file = os.path.join(dirname, 'OLED_SSD1306_128x64', 'resources/FreeSans.ttf')
    image_file = os.path.join(dirname, 'OLED_SSD1306_128x64', 'resources/pi_logo.png')


    i2cbus = SMBus(1)        # 1 = Raspberry Pi but NOT early REV1 board
    display = ssd1306(i2cbus)   # create oled object, nominating the correct I2C bus, default address

    font = ImageFont.truetype(font_file, 14)
    logo = Image.open(image_file)

    # "draw" onto this canvas, then call flush() to send the canvas contents to the hardware.
    canvas = display.canvas

    canvas.rectangle((0, 0, display.width-1, display.height-1), outline=1, fill=1)
    canvas.bitmap((32, 0), logo, fill=0)
    display.flush()
    time.sleep(4)

    ip_address = get_ip_address('eth0')

    # put border around the screen:
    display.canvas.rectangle((0, 0, display.width-1, display.height-1), outline=1, fill=0)

    # Write IP address to display
    canvas.text((8, 14), 'My IP Address is:', font=font, fill=1)
    canvas.text((8, 34), ip_address, font=font, fill=1)
    display.flush()

if __name__ == "__main__":
    sys.exit(main())
