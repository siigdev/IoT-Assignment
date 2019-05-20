import pycom
import time

ONE_THIRD = 1.0/3.0
ONE_SIXTH = 1.0/6.0
TWO_THIRD = 2.0/3.0

def rgb_to_hls(r, g, b):
    maxc = max(r, g, b)
    minc = min(r, g, b)
    # XXX Can optimize (maxc+minc) and (maxc-minc)
    l = (minc+maxc)/2.0
    if minc == maxc:
        return 0.0, l, 0.0
    if l <= 0.5:
        s = (maxc-minc) / (maxc+minc)
    else:
        s = (maxc-minc) / (2.0-maxc-minc)
    rc = (maxc-r) / (maxc-minc)
    gc = (maxc-g) / (maxc-minc)
    bc = (maxc-b) / (maxc-minc)
    if r == maxc:
        h = bc-gc
    elif g == maxc:
        h = 2.0+rc-bc
    else:
        h = 4.0+gc-rc
    h = (h/6.0) % 1.0
    return h, l, s

def hls_to_rgb(h, l, s):
    if s == 0.0:
        return l, l, l
    if l <= 0.5:
        m2 = l * (1.0+s)
    else:
        m2 = l+s-(l*s)
    m1 = 2.0*l - m2
    return (_v(m1, m2, h+ONE_THIRD), _v(m1, m2, h), _v(m1, m2, h-ONE_THIRD))

def _v(m1, m2, hue):
    hue = hue % 1.0
    if hue < ONE_SIXTH:
        return m1 + (m2-m1)*hue*6.0
    if hue < 0.5:
        return m2
    if hue < TWO_THIRD:
        return m1 + (m2-m1)*(TWO_THIRD-hue)*6.0
    return m1

def convert_rgb_to_hls(r, g, b):
    h, l, s = rgb_to_hls(r/255, g/255, b/255)
    return int(round(h * 359)), int(round(l * 100)), int(round(s * 100))

def convert_hls_to_rgb(h, l, s):
    r, g, b = hls_to_rgb(h/359, l/100, s/100)
    return int(round(r * 255)), int(round(g * 255)), int(round(b * 255))

def rgb_to_hex(red, green, blue):
    return '0x'+'%02x%02x%02x' % (red, green, blue)

def changeBrightness(r, g, b, brightness):
    hls = list(convert_rgb_to_hls(r, g, b))
    hls[1] = brightness
    rgb = convert_hls_to_rgb(hls[0], hls[1], hls[2])
    return int(rgb_to_hex(rgb[0], rgb[1], rgb[2]))


pycom.heartbeat(False)

for i in range(100): # stop after 10 cycles
    pycom.rgbled(changeBrightness(10, 50, 10, (100-i)))
    time.sleep(0.1)
