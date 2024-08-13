# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Audio Out WAV example"""
import time
import board
import digitalio
from audiocore import WaveFile

from rainbowio import colorwheel
import neopixel

print("letsgooo")

pixels = neopixel.NeoPixel(board.NEOPIXEL, 2, brightness=0.1, auto_write=False)

import adafruit_dotstar as dotstar
num_pixels = 100
dots = dotstar.DotStar(board.SCK, board.MOSI, num_pixels, brightness=0.2)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
dots.fill(CYAN)

def rainbow_cycle(wait):
    for j in range(255):
        pixels.fill(colorwheel(j))
        pixels.show()
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            dots[i] = colorwheel(rc_index & 255)
        #dots.show()
        time.sleep(wait)

def show_colour(color):
    pixels.fill(color)
    pixels.show()

while True:
    rainbow_cycle(0)  # Increase the number to slow down the rainbow

try:
    from audioio import AudioOut
    print("Found audioio")
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
        print("Found audiopwmio")
    except ImportError:
        print("Couldn't audio")
        pass  # not always supported by every board!

button = digitalio.DigitalInOut(board.A1)
button.switch_to_input(pull=digitalio.Pull.UP)

show_colour(BLUE)
print("looking for chicken")
wave_file = open("meow1.wav", "rb")
wave = WaveFile(wave_file)
audio = AudioOut(board.A0)


while True:
    print("let's go")
    show_colour(CYAN)
    audio.play(wave)
    print("i play it")

    show_colour(YELLOW)
    # This allows you to do other things while the audio plays!
    t = time.monotonic()
    while time.monotonic() - t < 6:
        pass

    show_colour(GREEN)
    audio.pause()
    print("Waiting for button press to continue!")
    while button.value:
        pass
    audio.resume()
    while audio.playing:
        pass
    print("Done!")
