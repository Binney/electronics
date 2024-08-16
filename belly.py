import time
import random
import board
import keypad

from audioio import AudioOut
from audiomp3 import MP3Decoder
from audiobusio import I2SOut

from rainbowio import colorwheel
from neopixel import NeoPixel
from adafruit_dotstar import DotStar

print("letsgooo")

pixels = NeoPixel(board.NEOPIXEL, 2, brightness=0.1, auto_write=False)

num_pixels = 118 # I don't even know
dots = DotStar(board.SCK, board.MOSI, num_pixels, brightness=0.2, auto_write=False)

RED = (255, 0, 0)
ORANGE = (255, 50, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
PINK = (255, 75, 150)
WHITE = (255, 255, 255)
NOTHING = (0, 0, 0)

def rainbow_cycle(wait):
    for j in range(255):
        pixels.fill(colorwheel(j))
        pixels.show()
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            dots[i] = colorwheel(rc_index & 255)
        dots.show()
        time.sleep(wait)

def show_colour(color):
    pixels.fill(color)
    pixels.show()
    dots.fill(color)
    dots.show()

def sweeping_clear(wait):
    for i in range(num_pixels):
        dots[i] = NOTHING
        dots.show()
        time.sleep(wait)

hue_offset = 0
def fill_to(pix):
    for i in range(pix, num_pixels):
        rc_index = (i * 256 // num_pixels) + hue_offset
        dots[i] = colorwheel(rc_index & 255)
    hue_offset += 1

rainbow_cycle(0)  # Increase the number to slow down the rainbow

def lerp(a, b, x):
    return a + (b - a) * x;

def colour_interp(col1, col2, x):
    (r1, g1, b1) = col1
    (r2, g2, b2) = col2
    return (lerp(r1, r2, x), lerp(g1, g2, x), lerp(b1, b2, x))

def fade_colours(palette):
    p = len(palette)
    for j in range(0, num_pixels):
        for i in range(0, num_pixels // p):
            for k in range(p):
                dots[(i + j + (k * num_pixels // p)) % num_pixels] = colour_interp(palette[k], palette[(k + 1) % p], i * p / num_pixels)
            dots.show()

def fluoresce():
    fade_colours([GREEN, BLUE])

def trans_pride():
    show_colour(PINK)
    print("yes!", num_pixels)
    fade_colours([PINK, CYAN, WHITE])
    time.sleep(10)

def sparkle():
    show_colour(PURPLE)

def glitter():
    show_colour(WHITE)
    
def glow():
    fade_colours([RED, ORANGE, YELLOW])
glow()

keys = keypad.Keys((board.A0, board.A1, board.A2,board.A3,board.A4, board.A5), value_when_pressed=False, pull=True)

mp3_file = open("RGSS.mp3", "rb")
decoder = MP3Decoder(mp3_file)
audio = I2SOut(board.D1, board.D10, board.D11)

def play_take_on_me():
    show_colour(YELLOW)
    print("playinggg")
    decoder.file = open("RGSS.mp3", "rb")
    audio.play(decoder)
    while audio.playing:
        pass
    show_colour(BLUE)
    sweeping_clear(0.1)
    print("done")

def shuffle_answer():
    numbers = ""
    for i in range(6):
        numbers += str(i)
    result = ""
    while numbers != "":
        char = random.choice(numbers)
        result += char
        numbers = numbers.replace(char, "")
        time.sleep(0.1)
    print("The answer is:", result)
    return result

show_colour(NOTHING)

correct_answer = "0123456"
sequence_to_enter = correct_answer

last_keypress_heard = 0

while True:
    if sequence_to_enter != correct_answer:
        # You got at least some of them right
        pix = ((len(correct_answer) - len(sequence_to_enter)) * num_pixels) // len(correct_answer)
        print("fill_to", len(correct_answer), len(sequence_to_enter), pix)
        for i in range(num_pixels - pix, num_pixels):
            rc_index = (i * 256 // num_pixels) + hue_offset
            dots[i] = colorwheel(rc_index & 255)
        dots.show()
        hue_offset += 1

    event = keys.events.get()
    # event will be None if nothing has happened.
    if event:
        print(event)
        print(event.timestamp)
        if event.pressed:
            if sequence_to_enter[0] == str(event.key_number):
                print("Correct!")
                sequence_to_enter = sequence_to_enter[1:]
            else:                
                print("Wrong")
                show_colour(NOTHING)
            if sequence_to_enter == "":
                print("Unlocked the Secret Mode!")
                # Celebrate:
                rainbow_cycle(0)
                play_take_on_me()
                # Restart game:
                sequence_to_enter = correct_answer
            last_keypress_heard = time.monotonic()
        print(event.released, time.monotonic() - last_keypress_heard)
        if event.released and time.monotonic() - last_keypress_heard > 10:
            # 0 starts the sequence, ignore that
            if event.key_number == 1:
                fluoresce()
            if event.key_number == 2:
                trans_pride()
            if event.key_number == 3:
                sparkle()
            if event.key_number == 4:
                glitter()
            if event.key_number == 5:
                glow()
    time.sleep(0.01)
