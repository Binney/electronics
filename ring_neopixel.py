from time import sleep
import board
import neopixel

num_pixels = 30

pixels = neopixel.NeoPixel(board.D18, num_pixels, pixel_order=neopixel.GRBW)
pixels.brightness = 0.1

def to_ints(input):
    return tuple(int(tup) for tup in input)

def hue_to_rgbw(hue):
    h = hue / 360.0
    v = 255.0
    s = 1.0
    i = int(h*6.0)
    f = h*6.0 - i
    a = 0.0
    
    w = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))

    if i==0: return to_ints((v, t, w, a))
    if i==1: return to_ints((q, v, w, a))
    if i==2: return to_ints((w, v, t, a))
    if i==3: return to_ints((w, q, v, a))
    if i==4: return to_ints((t, w, v, a))
    if i==5: return to_ints((v, w, q, a))

offset = 0

while True:
    pixels.fill(hue_to_rgbw(float(offset)))
    pixels[offset % 30] = (0, 0, 0, 255)
    sleep(0.01)
    offset += 1
    if offset >= 360:
        offset = 0
