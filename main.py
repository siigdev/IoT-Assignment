import pycom
import time
import colorconvert as ccv
from brightness import Brightness
from network import WLAN
import machine
from machine import Pin
import socket
from wifi_info import SSID, KEY
from umqtt import MQTTClient
from mqtt_info import SERVER, USER, PASSWORD, PORT

wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()
print(nets)
for net in nets:
    if net.ssid == SSID:
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, KEY), timeout=5000)
        while not wlan.isconnected():
            machine.idle()  # save power while waiting
        print('WLAN connection succeeded!')
        break

def sub_led(topic, msg):
    msg = str(msg).replace("'","")
    mode = msg.split(':')[1]
    r, g, b = stringbuildRgb(msg.split(':')[0])
    if (mode == "breathe"):
        breathe(r, g, b)
    elif (mode == "party"):
        party()
    elif (mode == "automatic"):
        automaticBrightness(r, g, b)
    elif (mode == "brightness"):
        bright = msg.split(':')[2]
        pycom.rgbled(changeBrightness(r, g, b, bright))

def stringbuildRgb(rgb):
    x = rgb[rgb.find('(')+1: rgb.find(')')]
    splitted = x.split(", ")
    return splitted[0], splitted[1], splitted[2]

client = MQTTClient('UNIQUENAME', SERVER, PORT, user=USER, password=PASSWORD)

def settimeout(duration): pass

client.settimeout = settimeout
client.set_callback(sub_led)
client.connect()
client.subscribe(b'/led')

def changeBrightness(r, g, b, brightness):
    r, g, b = int(r), int(g), int(b)
    brightness = int(brightness)
    hls = list(ccv.convert_rgb_to_hls(r, g, b))  # Convert to HLS
    hls[1] = brightness  # Set the brightness
    rgb = ccv.convert_hls_to_rgb(hls[0], hls[1], hls[2])  # Convert back to rgb
    # Convert to hex and return
    return int(ccv.rgb_to_hex(rgb[0], rgb[1], rgb[2]))

def changeColor(r, g, b):
    return int(ccv.rgb_to_hex(r, g, b))

def senseBrightness():
    return Brightness().light()[0]

def automaticBrightness(r, g, b):
    lux = senseBrightness()
    time.sleep(1)
    brightvalue = lux/10
    if lux > 1000:
        pycom.rgbled(changeBrightness(r, g, b, 0))
    else:
        pycom.rgbled(changeBrightness(r, g, b, 100-brightvalue))

def eventTimer(timer, event):
    while timer:
        time.sleep(1)
        timer -= 1
    print(event)

def breathe(r, g, b):
    i = 0
    countdown = False
    while True:
        pycom.rgbled(changeBrightness(r, g, b, i))
        time.sleep(0.03)
        if countdown == False:
            i += 1
            if (i >= 60):
                countdown = True
        if countdown == True:
            i -= 1
            if (i <= 0):
                countdown = False

def party():
    breatheval = False
    while True:
        pycom.rgbled(changeColor(255, 0, 0))
        time.sleep(1)
        pycom.rgbled(changeColor(0, 255, 255))
        time.sleep(1)
        pycom.rgbled(changeColor(255, 255, 0))
        time.sleep(1)
        pycom.rgbled(changeColor(0, 255, 0))
        time.sleep(1)
        pycom.rgbled(changeColor(255, 0, 255))
        time.sleep(1)
        pycom.rgbled(changeColor(0, 0, 255))
        time.sleep(1)

pycom.heartbeat(False)
while True:
    client.check_msg()
