import network
import socket
import ure
import time

wlan_sta = network.WLAN(network.STA_IF)
wlan_ap = network.WLAN(network.AP_IF)

def send_response(client, payload, status_code=200):
    client.sendall("HTTP/1.0 {} OK\r\n".format(status_code))
    client.sendall("Content-Type: text/html\r\n")
    client.sendall("Content-Length: {}\r\n".format(len(payload)))
    client.sendall("\r\n")
    
    if len(payload) > 0:
        client.sendall(payload)

def handle_root(client):
    response_header = """
        <h1>Wi-Fi Client Setup</h1>
        <form action="configure" method="post">
          <label for="ssid">SSID</label>
          <select name="ssid" id="ssid">
    """
    
    response_variable = ""
    turned_on = False
    if not wlan_sta.active():
        wlan_sta.active(True)
        turned_on = True
    for ssid, *_ in wlan_sta.scan():
        response_variable += '<option value="{0}">{0}</option>'.format(ssid.decode("utf-8"))
    if turned_on:
        wlan_sta.active(False)
        
    response_footer = """
           </select> <br/>
           Password: <input name="password" type="password"></input> <br />
           <input type="submit" value="Submit">
         </form>
    """
    send_response(client, response_header + response_variable + response_footer)

def handle_configure(client, request):
    match = ure.search("ssid=([^&]*)&password=(.*)", request)
    
    if match is None:
        send_response(client, "Parameters not found", status_code=400)
        return
    
    ssid = match.group(1)
    password = match.group(2)
    
    if len(ssid) == 0:
        send_response(client, "SSID must be provided", status_code=400)
        return
    
    wlan_sta.active(True)
    wlan_sta.connect(ssid.replace("+", " "), password)
    
    send_response(client, "Wi-Fi configured for SSID {}".format(ssid))
    return
    

def handle_not_found(client, url):
    send_response(client, "Path not found: {}".format(url), status_code=404)

def start(hw):
    wlan_sta.active(False)
    wlan_ap.active(True)
    wlan_ap.config(essid='TrumpBox')
    
    server_socket = socket.socket()
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(addr)
    server_socket.listen(1)

    print('listening on', addr)

    hw.oled.fill(0)
    hw.oled.text('Connect to...',0,0)
    hw.oled.text('TrumpBox',16,12)
    hw.oled.text('Browse to...',0,24)
    hw.oled.text('192.168.4.1',16,36)
    hw.oled.show()
    
    while True:
        client, addr = server_socket.accept()
        client.settimeout(5.0)
        print('client connected from', addr)
        
        request = b""
        try:
            while not "\r\n\r\n" in request:
                request += client.recv(512)
        except OSError:
            pass
        
        print("Request is: {}".format(request))
        if "HTTP" not in request:
            client.close()
            continue
        
        url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request).group(1).rstrip("/")
        print("URL is {}".format(url))
        
        finished = False
        if url == "":
            handle_root(client)
        elif url == "configure":
            handle_configure(client, request)
            finished = True
        else:
            handle_not_found(client, url)
        
        client.close()

        if finished:
            hw.oled.fill(0)
            hw.oled.text('Connecting...',0,0)
            hw.oled.show()
            break
        
    server_socket.close()
    server_socket = None
    client = None
    addr = None
    request = None
    url = None
    finished = None

    import machine
    machine.reset()
