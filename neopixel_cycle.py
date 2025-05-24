from time import sleep
import board
import neopixel

num_pixels = 30

pixels = neopixel.NeoPixel(board.GP3, num_pixels)#, pixel_order=neopixel.GRBW)
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

min_hue = 160
max_hue = 300

while True:
    for i in range(num_pixels):
        n = (i + offset) % num_pixels
        if n < num_pixels / 2:
            # go up
            huu = float(n) * 2 * (max_hue - min_hue) / num_pixels + min_hue
        else:
            huu = float(num_pixels - n) * 2 * (max_hue - min_hue) / num_pixels + min_hue
        pixels[i] = hue_to_rgbw(float(huu) % 360)
    sleep(0.01)
    offset += 1
    if offset > num_pixels:
        offset = 0
