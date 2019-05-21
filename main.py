import pycom
import time
import colorconvert as ccv
from brightness import Brightness

color = 0, 255, 0

def senseBrightness():
    return Brightness().light()[0]

def automaticBrightness():
    while True:
        lux = senseBrightness()
        time.sleep(1)
        brightvalue = lux/10
        print(brightvalue)
        if lux > 1000:
            pycom.rgbled(changeBrightness(255, 0, 0, 0))
        else:
            pycom.rgbled(changeBrightness(255, 0, 0, 100-brightvalue))
        

automaticBrightness()

def changeBrightness(r, g, b, brightness):
    hls = list(ccv.convert_rgb_to_hls(r, g, b)) # Convert to HLS
    hls[1] = brightness # Set the brightness
    rgb = ccv.convert_hls_to_rgb(hls[0], hls[1], hls[2]) #Convert back to rgb
    return int(ccv.rgb_to_hex(rgb[0], rgb[1], rgb[2])) # Convert to hex and return

def changeColor(r, g, b):
    return int(ccv.rgb_to_hex(r, g, b))

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

