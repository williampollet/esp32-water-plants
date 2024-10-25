import ubinascii
import machine
import time
import network
from umqtt.simple import MQTTClient

from amp import start_web_server, connect_to_wifi
from pumps import get_pump
from sensors import read_sensors, AdcConfig
from pumps import PumpConfig


#####################################################
# Set up AP Mode
#####################################################

ap = network.WLAN(network.AP_IF)
wifi = network.WLAN(network.STA_IF)
ap.config(essid="ESP32-Setup", authmode=network.AUTH_WPA_WPA2_PSK, password="password123")
ap.active(True)

#####################################################
# WiFi connect
#####################################################
if not connect_to_wifi(ap=ap, wifi=wifi):
    print("Failed to auto-connect. Starting AP mode for manual setup.")
    start_web_server(ap=ap, wifi=wifi)

#####################################################
# MQTT Configuration
#####################################################
client_id = ubinascii.hexlify(machine.unique_id())
mqtt_server = "192.168.0.42"
mqtt_port = 1883
mqtt_user = ""
mqtt_password = ""

# Initialize MQTT client
mqtt_client = MQTTClient(client_id, mqtt_server, mqtt_port)
mqtt_client.connect()

#####################################################
# Sensors configuration
#####################################################

# Setup a timer to read sensor values every 60 seconds
adc_config = AdcConfig()
timer = machine.Timer(0)

def periodic_sensor_read(timer):
    """
    Timer function to read sensor values every minute
    """
    global adc_config
    global mqtt_client

    read_sensors(mqtt_client=mqtt_client, adc_config=adc_config)

# Start the timer to read sensor values
timer.init(period=10000, mode=machine.Timer.PERIODIC, callback=periodic_sensor_read)

#####################################################
# Pump configuration
#####################################################

pump_config = PumpConfig()

def trigger_pump(topic, msg, _mqtt_client):
    """
    Callback function for MQTT messages
    """
    global pump_config
    print(f"Received message: {msg} on topic: {topic}")
    if topic == pump_config.pump_control_topic:
        pump, pump_time = get_pump(msg, pump_config)
        pump.on()
        time.sleep(pump_time)
        pump.off()

# Subscribe to the pump control topic
mqtt_client.set_callback(trigger_pump)
mqtt_client.subscribe(pump_config.pump_control_topic)
print(f"Subscribed to {pump_config.pump_control_topic}")

#####################################################
# Main loop
#####################################################
try:
    while True:
        mqtt_client.check_msg()
        time.sleep(1)  # Avoid busy-waiting
except KeyboardInterrupt:
    print("Program stopped")
finally:
    mqtt_client.disconnect()
    timer.deinit()
