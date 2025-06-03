import network

# WiFi Configuration
WIFI_SSID = "Networks"
WIFI_PASSWORD = "Network123#"
WIFI_MAX_RETRIES = 5
WIFI_RETRY_DELAY = 5000  # ms

# MQTT Configuration
MQTT_BROKER = 'broker.emqx.io'
MQTT_PORT = 1883

def get_unique_client_id():
    mac = network.WLAN().config('mac')
    return b'iot-soilmoisture_' + ''.join(['{:02x}'.format(b) for b in mac])

MQTT_CLIENT_ID = get_unique_client_id()
MQTT_TOPIC_PUBLISH = "iot-soilmoisture/data-sensor"
MQTT_TOPIC_SUBSCRIBE = "esp32/sensor"
MQTT_KEEPALIVE = 60

# Sensor Configuration
SOIL_MOISTURE_PIN = 35
DHT22_PIN = 17
RELAY_PIN = 27

# Sampling Interval
SENSOR_READ_INTERVAL = 30000  # 30 detik
SYNC_INTERVAL = 60000  # 1 menit

# Soil Moisture Thresholds
SOIL_DRY = 30  # <30% = kering
SOIL_WET = 60  # >60% = basah
# 30-60% = normal