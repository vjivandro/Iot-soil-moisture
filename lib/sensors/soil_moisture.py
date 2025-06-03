from machine import ADC, Pin
import config

class SoilMoisture:
    def __init__(self, pin):
        self.adc = ADC(Pin(pin))
        self.adc.atten(ADC.ATTN_11DB)  # Full range: 3.3v
        
    def read(self):
        """Membaca kelembapan tanah (0-100%)"""
        raw_value = self.adc.read()
        # Konversi ke persentase (sesuaikan dengan kalibrasi sensor Anda)
        percentage = 100 - ((raw_value / 4095) * 100)
        return round(percentage, 1)