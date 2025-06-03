from .lcd_api import LcdApi
from machine import I2C
import time

# constants
LCD_ADDR = 0x27
LCD_BACKLIGHT = 0x08
ENABLE = 0x04
CMD = 0
DATA = 1

class I2cLcd(LcdApi):
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.num_lines = num_lines
        self.num_columns = num_columns
        super().__init__(num_lines, num_columns)
        self.init_lcd()

    def init_lcd(self):
        self.send_command(0x33)
        self.send_command(0x32)
        self.send_command(0x28)
        self.send_command(0x0C)
        self.send_command(0x06)
        self.clear()

    def send_command(self, cmd):
        self.send_byte(cmd, CMD)

    def send_data(self, data):
        self.send_byte(data, DATA)

    def send_byte(self, data, mode):
        high = mode | (data & 0xF0) | LCD_BACKLIGHT
        low = mode | ((data << 4) & 0xF0) | LCD_BACKLIGHT
        self.i2c.writeto(self.i2c_addr, bytes([high | ENABLE]))
        self.i2c.writeto(self.i2c_addr, bytes([high]))
        self.i2c.writeto(self.i2c_addr, bytes([low | ENABLE]))
        self.i2c.writeto(self.i2c_addr, bytes([low]))
        time.sleep_ms(1)

    def move_to(self, col, row):
        row_offsets = [0x00, 0x40, 0x14, 0x54]
        self.send_command(0x80 | (col + row_offsets[row]))

    def putchar(self, char):
        self.send_data(ord(char))

