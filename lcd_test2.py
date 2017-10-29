from Adafruit_CharLCD import Adafruit_CharLCD
import Adafruit_GPIO.PCF8574 as PCF
import time

gpio = PCF.PCF8574(address=0x3f)

# Define PCF pins connected to the LCD.
lcd_rs        = 0
lcd_rw        = 1
lcd_en        = 2
lcd_backlight = 3
d4,d5,d6,d7   = 4,5,6,7
cols,lines    = 16,2

gpio.setup(lcd_rw, PCF.OUT)
gpio.output(lcd_rw, 0)

# Instantiate LCD Display
lcd = Adafruit_CharLCD(lcd_rs, lcd_en, d4, d5, d6, d7, cols, lines,
                       lcd_backlight, invert_polarity=False, gpio=gpio)

# Demo scrolling message right/left.
lcd.clear()
message = 'Scroll'
lcd.message(message)
for i in range(cols - len(message)):
    time.sleep(0.5)
    lcd.move_right()
for i in range(cols - len(message)):
    time.sleep(0.5)
    lcd.move_left()

# Demo turning backlight off and on.
lcd.clear()
lcd.message('Flash backlight\nin 5 seconds...')
time.sleep(5.0)
# Turn backlight off.
lcd.set_backlight(0)
time.sleep(2.0)
# Change message.
lcd.clear()
lcd.message('Goodbye!')
# Turn backlight on.
lcd.set_backlight(1)
