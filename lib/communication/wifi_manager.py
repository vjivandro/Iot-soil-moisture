import network
import time
from lib.utils import Logger

class WiFiManager:
    def __init__(self, ssid, password, max_retries=5, retry_delay=5000):
        self.ssid = ssid
        self.password = password
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.wlan = network.WLAN(network.STA_IF)
        self.logger = Logger()
        
    def connect(self):
        if not self.wlan.isconnected():
            # Reset interface WiFi
            self.wlan.active(False)
            time.sleep_ms(500)
            self.wlan.active(True)
            
            # Connect dengan SSID dan password Anda
            self.wlan.connect(self.ssid, self.password)
            
            retries = 0
            while retries < self.max_retries:
                if self.wlan.isconnected():
                    self.logger.info("WiFi connected!")
                    self.logger.info("IP:", self.wlan.ifconfig()[0])
                    return True
                
                self.logger.debug(f"Connecting... ({retries+1}/{self.max_retries})")
                time.sleep_ms(self.retry_delay)
                retries += 1
            
            self.logger.error("Failed to connect to WiFi")
            return False
        return True
        
    def is_connected(self):
        return self.wlan.isconnected()