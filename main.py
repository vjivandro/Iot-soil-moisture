# main.py -- put your code here!
import time
from machine import Pin, I2C
from lib.sensors import SoilMoisture, DHT22
from lib.actuators import Relay, LCD_I2C
from lib.communication import WiFiManager, MQTTClientWrapper
from lib.storage import LocalStorage
from lib.utils import Logger
import config
import secrets

# Inisialisasi komponen
logger = Logger()
wifi = WiFiManager(config.WIFI_SSID, config.WIFI_PASSWORD, config.WIFI_MAX_RETRIES, config.WIFI_RETRY_DELAY)
mqtt = MQTTClientWrapper(
    config.MQTT_BROKER, 
    str(config.MQTT_PORT),  # Konversi port ke string
    config.MQTT_CLIENT_ID, 
    secrets.MQTT_USER, 
    secrets.MQTT_PASSWORD
)
storage = LocalStorage()

# Inisialisasi sensor dan aktuator
soil_sensor = SoilMoisture(config.SOIL_MOISTURE_PIN)
dht_sensor = DHT22(config.DHT22_PIN)
relay = Relay(config.RELAY_PIN)
i2c = I2C(scl=Pin(22), sda=Pin(21))
lcd = LCD_I2C(i2c)

last_read_time = 0
last_sync_time = 0

def read_sensors():
    """Membaca semua sensor dan mengembalikan data dalam dictionary"""
    soil = soil_sensor.read()
    dht_data = dht_sensor.read()
    
    return {
        "soil_moisture": soil,
        "temperature": dht_data["temperature"],
        "humidity": dht_data["humidity"],
        "timestamp": time.time()
    }

def control_irrigation(soil_moisture):
    """Mengontrol penyiraman berdasarkan kelembapan tanah"""
    if soil_moisture < config.SOIL_DRY - 5:
        relay.on()
        status = "K"
    elif soil_moisture > config.SOIL_WET + 5:
        relay.off()
        status = "B"
    else:
        relay.off()
        status = "N"
    
    return status

def display_data(data, irrigation_status):
    """Menampilkan data di LCD"""
    lcd.clear()
    lcd.putstr(f"SM: {data['soil_moisture']}% ({irrigation_status})")
    logger.debug(f"Soil: {data['soil_moisture']}% ({irrigation_status})")
    lcd.move_to(0, 1)
    lcd.putstr(f"T: {data['temperature']}C H: {data['humidity']}%")
    logger.debug(f"T: {data['temperature']}C H: {data['humidity']}%")

def sync_data():
    """Menyinkronkan data lokal dengan cloud ketika terkoneksi"""
    if wifi.is_connected():
        unsynced_data = storage.get_unsynced_data()
        for data in unsynced_data:
            if mqtt.publish(config.MQTT_TOPIC_PUBLISH, data):
                logger.info("Data synced successfully:", data)
                storage.mark_as_synced(data["id"])
            else:
                logger.error("Failed to sync data:", data)

def main_loop():
    global last_read_time, last_sync_time
    
    current_time = time.ticks_ms()
    
    # Baca sensor secara berkala
    if time.ticks_diff(current_time, last_read_time) >= config.SENSOR_READ_INTERVAL:
        sensor_data = read_sensors()
        irrigation_status = control_irrigation(sensor_data["soil_moisture"])
        display_data(sensor_data, irrigation_status)
        
        # Simpan data ke penyimpanan lokal
        storage.save_data(sensor_data)
        
        last_read_time = current_time
    
    # Sinkronisasi data secara berkala
    if time.ticks_diff(current_time, last_sync_time) >= config.SYNC_INTERVAL:
        sync_data()
        last_sync_time = current_time
    
    time.sleep_ms(100)

# Main execution
if __name__ == "__main__":
    wifi.connect()
    if wifi.is_connected():
        try:
            mqtt.connect()
            logger.info("MQTT connected successfully")
        except Exception as e:
            logger.error(f"MQTT connection failed: {e}")
    
    while True:
        main_loop()