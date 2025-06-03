from machine import I2C, Pin
from lib.utils.i2c_lcd import I2cLcd  

class LCD_I2C:
    def __init__(self, i2c, address=0x27, rows=2, cols=16):
        self.lcd = I2cLcd(i2c, address, rows, cols)
        
    def clear(self):
        self.lcd.clear()
        
    def putstr(self, text):
        self.lcd.putstr(text)
        
    def move_to(self, col, row):
        self.lcd.move_to(col, row)