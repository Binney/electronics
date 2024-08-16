# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Audio Out WAV example"""
import time
import board
import digitalio
from audiocore import WaveFile

import busio
import sdcardio
import storage

from rainbowio import colorwheel
import neopixel

print("letsgooo")

# Use the board's primary SPI bus
spi = board.SPI()
# Or, use an SPI bus on specific pins:
#spi = busio.SPI(board.SD_SCK, MOSI=board.SD_MOSI, MISO=board.SD_MISO)

# For breakout boards, you can choose any GPIO pin that's convenient:
cs = board.D9
# Boards with built in SPI SD card slots will generally have a
# pin called SD_CS:
#cs = board.SD_CS

sdcard = sdcardio.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

with open("/sd/test.txt", "w") as f:
    f.write("Hello world!\r\n")

pixels = neopixel.NeoPixel(board.NEOPIXEL, 2, brightness=0.1, auto_write=False)

import adafruit_dotstar as dotstar
num_pixels = 118 # I don't even know
#dots = dotstar.DotStar(board.SCK, board.MOSI, num_pixels, brightness=0.2, auto_write=False)
dots = dotstar.DotStar(board.D6, board.D5, num_pixels, brightness=0.2, auto_write=False)

RED = (255, 0, 0)
ORANGE = (255, 50, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

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

#button = digitalio.DigitalInOut(board.A1)
#button.switch_to_input(pull=digitalio.Pull.UP)

#show_colour(BLUE)

from audiomp3 import MP3Decoder
from audiobusio import I2SOut

print("looking for chicken")
mp3_file = open("RGSS.mp3", "rb")
decoder = MP3Decoder(mp3_file)
#audio = AudioOut(board.A1)
audio = I2SOut(board.D1, board.D10, board.D11)

def play_take_on_me():
    show_colour(YELLOW)
    print("playinggg")
    #file_to_play = open("/sd/RGSS.wav", "rb")
    #wave_file = WaveFile(file_to_play)
    #audio.play(wave_file)
    decoder.file = open("RGSS.mp3", "rb")
    audio.play(decoder)
    while audio.playing:
        pass
    show_colour(BLUE)
    print("done")

#while True:
play_take_on_me()
time.sleep(5)
