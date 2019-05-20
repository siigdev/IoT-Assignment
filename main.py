import pycom
import time
import colorconvert as ccv

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
        pycom.rgbled(changeBrightness(255, 50, 10, i))
        time.sleep(0.01)
        if countdown == False:
            i += 1
            if (i >= 100):
                countdown = True
        if countdown == True: 
            i -= 1
            if (i <= 0):
                countdown = False



pycom.heartbeat(False)

breathe(255, 50, 10)
#time.sleep(1)

