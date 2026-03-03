from time import sleep
import board
import busio
from adafruit_ht16k33.segments import Seg7x4
import neopixel
from adafruit_ticks import ticks_ms, ticks_add
import digitalio
from adafruit_debouncer import Debouncer

i2c = busio.I2C(board.GP3, board.GP2)
display = Seg7x4(i2c)
# display.print("9999")
# sleep(1)
# display.print("    ")
# sleep(0.5)

button = digitalio.DigitalInOut(board.GP1)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

debouncer = Debouncer(button)

num_pixels = 15

pixels = neopixel.NeoPixel(board.GP0, num_pixels)#, pixel_order=neopixel.GRBW)
pixels.brightness = 0.1

songs = [
    "the chances of anything stopping this party are 1 000 000 to 1, he said",
    "hit the floor and lets see you dance to ABBA",
    "Playing Bee Gees - Tragedy",
    "Playing Dua Lipa - Physical",
    "beep boop - party is here",
    "youve arrived at Panic Station",
    "bang your heads for the Prince - its o22y osbourne - Cra2y train - choo choo",
    "one final song"
]

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

hues = [
    [250, 290], # basically just purple
    [-45, 45], # pink to yellow
    [45, 180], # yellow to blue
    [160, 300], # blue to pink
    [100, 180], # blue and green
    [300, 370], # pink and orange
    [-10, 10], # basically just red
    [240, 250] # basically just blue
]

SLOW_LOOP_INTERVAL = 200  # milliseconds

last_fast = ticks_ms()
last_slow = ticks_ms()

leds_offset = 0
msg_offset = 0
current_song = 0

while True:
    current_time = ticks_ms()
    
    # Fast loop - runs as often as possible
    [min_hue, max_hue] = hues[current_song % len(hues)]
    for i in range(num_pixels):
        n = (i + leds_offset) % num_pixels
        if n < num_pixels / 2:
            # go up
            huu = float(n) * 2 * (max_hue - min_hue) / num_pixels + min_hue
        else:
            huu = float(num_pixels - n) * 2 * (max_hue - min_hue) / num_pixels + min_hue
        pixels[i] = hue_to_rgbw(float(huu) % 360)
    leds_offset += 1
    if leds_offset > num_pixels:
        leds_offset = 0

    debouncer.update()
    if debouncer.rose:
        print("skip")
        msg_offset = 0
        current_song = (current_song + 1) % len(songs)
    
    # Slow loop - runs every 200ms
    if ticks_add(current_time, -last_slow) >= SLOW_LOOP_INTERVAL:
        msg_offset += 1
        if msg_offset > len(songs[current_song]) + 5:
            msg_offset = 0
        message = f"   {songs[current_song]}    "
        display.print(message[msg_offset:4+msg_offset])
        last_slow = current_time
