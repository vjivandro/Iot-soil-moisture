import json
from umqtt.simple import MQTTClient 
from lib.utils import Logger

class MQTTClientWrapper:
    def __init__(self, broker, port, client_id, user=None, password=None, keepalive=60):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.user = user
        self.password = password
        self.keepalive = keepalive
        self.client = None
        self.logger = Logger()
        self.reconnect_delay = 5
        
    def connect(self):
        try:
            self.client = MQTTClient(
                client_id=self.client_id,
                server=self.broker,
                port=self.port,
                user=self.user,
                password=self.password,
                keepalive=self.keepalive
            )
            self.client.connect()
            self.logger.info("Connected to MQTT broker")
            return True
        except Exception as e:
            self.logger.error("MQTT connection error:", e)
            return False
            
    def disconnect(self):
        if self.client:
            self.client.disconnect()
            
    def publish(self, topic, message):
        try:
            if isinstance(message, dict):
                message = json.dumps(message)
            # Publish dengan QoS=1
            self.client.publish(topic, message)
            return True
        except Exception as e:
            self.logger.error("MQTT publish error:", e)
            return False
            
    def subscribe(self, topic, callback, qos=1):
        try:
            self.client.set_callback(callback)
            # Subscribe dengan QoS=1
            self.client.subscribe(topic, qos=qos)
            return True
        except Exception as e:
            self.logger.error("MQTT subscribe error:", e)
            return False
