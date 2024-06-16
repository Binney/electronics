import time
from pathlib import Path
import keyboard_input_emulators
# import rotary_phone_input
import logging
import os
import vlc

# Required on Windows; comment out on Pi
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')


logging.basicConfig(level=logging.INFO)
logging.getLogger('transitions').setLevel(logging.INFO)

vlc_ins = vlc.Instance()
player = vlc_ins.media_player_new()

vlc_ins = vlc.Instance()
player = vlc_ins.media_player_new()

sounds_directory = Path(__file__).parent / "sounds"
one_candle = vlc_ins.media_new(sounds_directory / "dialup-2a.mp3")
two_book = vlc_ins.media_new(sounds_directory / "dialup-3a.mp3")
three_bell = vlc_ins.media_new(sounds_directory / "dialup-6a.mp3")
four_glasses = vlc_ins.media_new(sounds_directory / "dialup-7a.mp3")
five_sun = vlc_ins.media_new(sounds_directory / "dialup-8a.mp3")
six_flower = vlc_ins.media_new(sounds_directory / "dialup-1a.mp3")
seven_radiation = vlc_ins.media_new(sounds_directory / "dialup-0a.mp3")
eight_righthand = vlc_ins.media_new(sounds_directory / "dialup-5a.mp3")
nine_lefthand = vlc_ins.media_new(sounds_directory / "dialup-9a.mp3")
zero_snowflake = vlc_ins.media_new(sounds_directory / "dialup-4a.mp3")

# noinspection PyUnresolvedReferences
class BinneyDialup(object):

    def __init__(self):
        self.dial_history = ""
        self.dial_callbacks = {}

        keyboard_input_emulators.set_up_keyboard_phone_emulator(self.dialled_digit, self.off_hook)
        # rotary_phone_input.set_up_phone_input(self.dialled_digit, self.off_hook)  123451
        self.dial_callbacks = {
            "1": self.play_one
        }

    def off_hook(self):
        player.stop()
        print("Phone off hook")

    def play_one(self):
        print("Playing 1")

    def dialled_digit(self, digit):
        print("Received digit: " + str(digit))

        if digit == 1:
            self.play_sound(one_candle)
        elif digit == 2:
            self.play_sound(two_book)
        elif digit == 3:
            self.play_sound(three_bell)
        elif digit == 4:
            self.play_sound(four_glasses)
        elif digit == 5:
            self.play_sound(five_sun)
        elif digit == 6:
            self.play_sound(six_flower)
        elif digit == 7:
            self.play_sound(seven_radiation)
        elif digit == 8:
            self.play_sound(eight_righthand)
        elif digit == 9:
            self.play_sound(nine_lefthand)
        elif digit == 0:
            self.play_sound(zero_snowflake)

    def play_sound(self, sound):
        player.stop()
        player.set_media(sound)
        player.play()

    def play_sound_with_delay(self, sound):
        time.sleep(2)
        self.play_sound(sound)


BinneyDialup()

while True:
    time.sleep(1)
