from machine import Pin

class Relay:
    def __init__(self, pin, active_low=False):
        self.pin = Pin(pin, Pin.OUT)
        self.active_low = active_low
        self.off()
        
    def on(self):
        """Menyalakan relay"""
        self.pin.value(0 if self.active_low else 1)
        
    def off(self):
        """Mematikan relay"""
        self.pin.value(1 if self.active_low else 0)
        
    def toggle(self):
        """Toggle relay"""
        self.pin.value(not self.pin.value())