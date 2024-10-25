import network
import time
from umqtt.simple import MQTTClient
import usocket as socket

ssid = 'freebox_VRRZOD'
password = 'lereseauwifideclemetwill2016'
CLIENT_NAME = 'blue'
BROKER_ADDR = '192.168.0.42'

def ping_host(host, port=1883, timeout=5):
    try:
        # Create a new socket
        s = socket.socket()
        s.settimeout(timeout)
        
        # Try to connect to the host and port
        s.connect((host, port))
        s.close()
        return True
    except OSError as e:
        print(f"Ping failed: {e}")
        return False


if __name__=="__main__":
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Try connect to SSID : {ssid}")
        wlan.connect(ssid, password)

        while not wlan.isconnected():
            print('.', end = " ")
            time.sleep_ms(500)

    time.sleep(2)  # Add a small delay before proceeding
    print("\nWi-Fi Config: ", wlan.ifconfig())

    mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)


    if ping_host(BROKER_ADDR):
        print(f"{BROKER_ADDR} is reachable.")
    else:
        print(f"{BROKER_ADDR} is not reachable.")
    try:
        mqttc.connect()
        print(f"Connected to {BROKER_ADDR}, waiting for messages")
        mqttc.publish("hello", "world")
        time.sleep_ms(500)
        mqttc.publish("hello", "world-2-man")
    except OSError as e:
        print(f"Connection failed: {e}")
