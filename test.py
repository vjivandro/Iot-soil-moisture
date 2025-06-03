import socket
import config
addr = socket.getaddrinfo(config.MQTT_BROKER, config.MQTT_PORT)[0][-1]
s = socket.socket()
try:
    s.connect(addr)
    print("Connected to broker")
except Exception as e:
    print("Socket connection failed:", e)
finally:
    s.close()
