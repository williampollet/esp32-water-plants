import network
import usocket as socket
import ujson
import time

def start_web_server(ap: network.WLAN, wifi: network.WLAN):
    # Set up a socket for HTTP requests
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Web server is running on http://192.168.4.1")
    
    response = ""
    while True:
        cl, addr = s.accept()
        print("Client connected from", addr)
        
        request = cl.recv(1024)
        print("Request:", request)
        if response == "<h2>WiFi credentials received. Connecting...</h2>":
            time.sleep(0.2)
            break

        # Check if the client is requesting the form submission
        if "POST /connect" in request:
            try:
                # Extract data from POST request
                data = request.decode().split("\r\n\r\n")[-1]
                print(data)
                creds = {c.split('=')[0]: c.split('=')[1] for c in data.split('&')}
                ssid = creds["ssid"]
                password = creds["password"]

                # Store the credentials and try connecting
                save_credentials(ssid, password)
                response = "<h2>WiFi credentials received. Connecting...</h2>"
                connect_to_wifi(ap=ap, wifi=wifi)
            except Exception as e:
                response = "<h2>Error processing credentials.</h2>"
        else:
            # Serve the HTML form to enter WiFi credentials
            response = """\
                <!DOCTYPE html>
                <html>
                <body>
                <h2>Connect ESP32 to WiFi</h2>
                <form action="/connect" method="post">
                    <label>SSID:</label><br>
                    <input type="text" name="ssid"><br>
                    <label>Password:</label><br>
                    <input type="password" name="password"><br><br>
                    <input type="submit" value="Connect">
                </form>
                </body>
                </html>
                """

        # Send response to client and close connection
        cl.send(response)
        cl.close()

def save_credentials(ssid, password):
    with open("wifi_creds.json", "w") as f:
        creds = {"ssid": ssid, "password": password}
        print(creds)
        f.write(ujson.dumps(creds))

def load_credentials():
    try:
        with open("wifi_creds.json", "r") as f:
            creds = ujson.loads(f.read())
            return creds["ssid"], creds["password"]
    except:
        return None, None

def connect_to_wifi(ap: network.WLAN, wifi: network.WLAN):
    wifi.active(True)

    # Load credentials if available
    ssid, password = load_credentials()
    if ssid and password:
        print("Connecting to WiFi...")
        wifi.connect(ssid, password)

        for i in range(10):  # Wait for connection
            if wifi.isconnected():
                print("Connected to WiFi:", ssid)
                print("IP Address:", wifi.ifconfig()[0])
                return True
            time.sleep(1)
        
        print("Failed to connect to WiFi.")
    return False
