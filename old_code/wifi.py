import time
import network

# Wifi credentials
ssid = 'freebox_VRRZOD'
password = 'lereseauwifideclemetwill2016'

def connect_wifi(ssid, password):
    """
    Connect to the WiFi network
    param ssid: str: The SSID of the WiFi network
    param password: str: The password of the WiFi network
    """
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(ssid, password)
    while not wifi.isconnected():
        print("Connecting to WiFi...")
        time.sleep(1)
    print("Connected to WiFi", wifi.ifconfig())

# Initialize the MQTT client
connect_wifi(ssid, password)
