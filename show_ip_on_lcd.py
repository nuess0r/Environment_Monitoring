from Adafruit_CharLCD import Adafruit_CharLCD
import Adafruit_GPIO.PCF8574 as PCF
import time
import socket
import fcntl
import struct

# Define PCF pins connected to the LCD.
lcd_rs        = 0
lcd_rw        = 1
lcd_en        = 2
lcd_backlight = 3
d4,d5,d6,d7   = 4,5,6,7
cols,lines    = 16,2


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


gpio = PCF.PCF8574(address=0x3f)

gpio.setup(lcd_rw, PCF.OUT)
gpio.output(lcd_rw, 0)

# Instantiate LCD Display
lcd = Adafruit_CharLCD(lcd_rs, lcd_en, d4, d5, d6, d7, cols, lines, 
                       lcd_backlight, invert_polarity=False, gpio=gpio)


ip_address = get_ip_address('eth0')

lcd.clear()
lcd.message('My IP address is\n' + ip_address)
lcd.set_backlight(1)
