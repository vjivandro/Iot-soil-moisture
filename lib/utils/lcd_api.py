class LcdApi:
    def __init__(self, num_lines, num_columns):
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.clear()

    def clear(self):
        self.move_to(0, 0)
        self.putstr(" " * self.num_columns * self.num_lines)
        self.move_to(0, 0)

    def move_to(self, col, row):
        pass  # implementasi di i2c_lcd

    def putstr(self, string):
        for char in string:
            self.putchar(char)

    def putchar(self, char):
        pass  # implementasi di i2c_lcd

