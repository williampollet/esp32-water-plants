import network
import time

ssid = 'freebox_VRRZOD'
password = 'lereseauwifideclemetwill2016'
CLIENT_NAME = 'blue'
BROKER_ADDR = '192.168.0.42'


def connect_wifi(ssid, password):
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(ssid, password)
    while not wifi.isconnected():
        print("Connecting to WiFi...")
        time.sleep(1)
    print("Connected to WiFi", wifi.ifconfig())

# Replace with your WiFi credentials
connect_wifi('your-ssid', 'your-password')
