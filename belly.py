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
PURPLE = (255, 0, 255)
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

def fill_rainbow_to(pix):
    for i in range(num_pixels - pix, num_pixels):
        rc_index = (i * 256 // num_pixels) + hue_offset
        dots[i] = colorwheel(rc_index & 255)
    dots.show()

def lerp(a, b, x):
    return a + (b - a) * x;

def colour_interp(col1, col2, x):
    (r1, g1, b1) = col1
    (r2, g2, b2) = col2
    return (lerp(r1, r2, x), lerp(g1, g2, x), lerp(b1, b2, x))

def fade_colours(palette):
    p = len(palette)
    for j in range(0, num_pixels):
        for i in range(num_pixels // p):
            for k in range(p):
                dots[(i + j + (k * num_pixels // p)) % num_pixels] = colour_interp(palette[k], palette[(k + 1) % p], i * p / num_pixels)
            dots.show()

def chaser(palette, chaser_size, wait):
    p = len(palette)
    for j in range(num_pixels):
        for i in range(num_pixels):
            dots[(i + j) % num_pixels] = palette[(i // chaser_size) % p]
        dots.show()
        time.sleep(wait)

def reset():
    show_colour(NOTHING)

def meadow():
    fade_colours([YELLOW, GREEN, CYAN, (0, 255, 50)])
    reset()

def trans_pride():
    chaser([PINK, CYAN, WHITE], 5, 0.05)
    reset()

def sunset():
    fade_colours([ORANGE, PURPLE, BLUE])
    reset()

def glitter():
    chaser([WHITE, NOTHING, NOTHING, PURPLE, NOTHING, NOTHING, WHITE, NOTHING, ORANGE, NOTHING], 3, 0.1)
    show_colour(WHITE)
    reset()

def glow():
    fade_colours([RED, ORANGE, YELLOW])
    reset()

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

reset()

correct_answer = "012345"
sequence_to_enter = correct_answer

last_keypress_heard = 0
last_button_pressed = -1

while True:
    if sequence_to_enter != correct_answer:
        # You got at least some of them right
        pix = ((len(correct_answer) - len(sequence_to_enter)) * num_pixels) // len(correct_answer)
        fill_rainbow_to(pix)
        hue_offset += 1

    event = keys.events.get()
    # event will be None if nothing has happened.
    if event:
        print(event)
        print(event.timestamp)
        if event.pressed:
            last_button_pressed = event.key_number
            if sequence_to_enter[0] == str(event.key_number):
                print("Correct!")
                sequence_to_enter = sequence_to_enter[1:]
            else:
                print("Wrong")
                sequence_to_enter = correct_answer
                reset()
            if sequence_to_enter == "":
                print("Unlocked the Secret Mode!")
                # Celebrate:
                rainbow_cycle(0)
                play_take_on_me()
                # Restart game:
                sequence_to_enter = correct_answer
            last_keypress_heard = time.monotonic()
        if event.released:
            last_button_pressed = -1

    if last_button_pressed > 0 and time.monotonic() - last_keypress_heard > 10:
        # 0 starts the sequence, ignore that
        if last_button_pressed == 1:
            meadow()
            last_button_pressed = -1
        if last_button_pressed == 2:
            trans_pride()
            last_button_pressed = -1
        if last_button_pressed == 3:
            sunset()
            last_button_pressed = -1
        if last_button_pressed == 4:
            glitter()
            last_button_pressed = -1
        if last_button_pressed == 5:
            glow()
            last_button_pressed = -1
    time.sleep(0.01)
