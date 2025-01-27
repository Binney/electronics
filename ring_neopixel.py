from time import sleep
import board
import neopixel

num_pixels = 16

pixels = neopixel.NeoPixel(board.GP0, num_pixels, pixel_order=neopixel.GRBW)
pixels.brightness = 0.1

def hue_to_rgbw(hue):
    h = hue / 360.0
    v = 255.0
    s = 1.0
    i = int(h*6.0)
    f = h*6.0 - i
    a = 0
    
    w = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))

    if i==0: return (v, t, w, a)
    if i==1: return (q, v, w, a)
    if i==2: return (w, v, t, a)
    if i==3: return (w, q, v, a)
    if i==4: return (t, w, v, a)
    if i==5: return (v, w, q, a)

offset = 0

while True:
    pixels.fill(hue_to_rgbw(offset))
    pixels[offset % 16] = (0, 0, 0, 255)
    sleep(0.01)
    offset += 1
    if offset >= 360:
        offset = 0
