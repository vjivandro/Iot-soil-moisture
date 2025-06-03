import dht
from machine import Pin
import time

class DHT22:
    def __init__(self, pin):
        self.sensor = dht.DHT22(Pin(pin))
        
    def read(self):
        """Membaca suhu dan kelembapan udara"""
        retries = 3
        for i in range(retries):
            try:
                self.sensor.measure()
                return {
                    "temperature": self.sensor.temperature(),
                    "humidity": self.sensor.humidity()
                }
            except Exception as e:
                if i == retries - 1:
                    return {"temperature": 0, "humidity": 0}
                time.sleep_ms(100)