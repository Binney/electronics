import time
from pathlib import Path
import keyboard_input_emulators
# import rotary_phone_input
# import door_input
from transitions import Machine
import logging
import os

import vlc

logging.basicConfig(level=logging.INFO)
logging.getLogger('transitions').setLevel(logging.INFO)


vlc_ins = vlc.Instance()
player = vlc_ins.media_player_new()

sounds_directory = Path(__file__).parent / "sounds"
loud_ringing_sound = vlc_ins.media_new(sounds_directory / "loud_ringing_sound.mp3")

# noinspection PyUnresolvedReferences
class Hallowpuzz(object):
    states = ['initial', 'puzzle_start', 'inputting_ghost_name', 'ouija_t', 'ouija_e', 'ouija_a', 'ouija_question_mark']

    def __init__(self):
        self.dial_history = ""
        self.dial_callbacks = {}

        self.machine = Machine(model=self, states=Hallowpuzz.states, initial='initial')

        self.machine.add_transition(trigger='start_puzzle', source=['initial', 'inputting_ghost_name'],
                                    dest='puzzle_start')
        self.machine.add_transition(trigger='start_inputting_ghost_name',
                                    source='puzzle_start ',
                                    dest='inputting_ghost_name')
        self.machine.add_transition(trigger='start_ouija',
                                    source=['inputting_ghost_name', 'ouija_t', 'ouija_e', 'ouija_a',
                                            'ouija_question_mark'],
                                    dest='ouija_t')
        self.machine.add_transition(trigger='move_to_ouija_e', source='ouija_t', dest='ouija_e')
        self.machine.add_transition(trigger='move_to_ouija_a', source='ouija_e', dest='ouija_a')
        self.machine.add_transition(trigger='move_to_ouija_question_mark', source='ouija_a', dest='ouija_question_mark')

        keyboard_input_emulators.set_up_keyboard_door_emulator(self.door_opened)
        # door_input.set_up_door_input(self.door_opened)
        keyboard_input_emulators.set_up_keyboard_phone_emulator(self.dialled_digit, self.off_hook)
        # rotary_phone_input.set_up_phone_input(self.dialled_digit, self.off_hook)

    def door_opened(self):
        print("Door opened")
        if self.is_initial():
            player.set_media(loud_ringing_sound)
            player.play()

    def off_hook(self):
        print("Phone off hook")
        if self.is_initial():
            print("Hello Mr Kearns; we are calling from Camden council etc etc. Please dial 1")
            self.start_puzzle()
        elif self.is_puzzle_start():
            print("To hear the ghost hunting info again, please dial 1; to input the name of your ghost, please dial 9")
        elif self.is_inputting_ghost_name():
            print("To hear the ghost hunting info again, please dial 1; to input the name of your ghost, please dial 9")
            self.start_puzzle()
        else:
            print("To hear the ghost hunting info again, please dial 1; to input the name of your ghost, please dial 9")
            self.start_puzzle()

    def dialled_digit(self, digit):
        print("Received digit: " + str(digit))
        self.dial_history += str(digit)
        print("Dial history: " + self.dial_history)
        callback = next((
            callback for sequence, callback in self.dial_callbacks.items() if self.dial_history.endswith(sequence)),
            None)
        if callback:
            self.dial_history = ""
            callback()

    def on_enter_puzzle_start(self):
        self.dial_callbacks = {
            "1": self.direct_to_book,
            "9": self.start_inputting_ghost_name
        }

    def on_enter_inputting_ghost_name(self):
        print("Please dial ghost name")
        self.dial_callbacks = {
            "254779": self.start_ouija,
            "0": self.start_puzzle
        }

    def on_enter_ouija_t(self):
        print("The ghost will tell you where to find its new body; follow what it's trying to tell you,"
              " and dial any letters into the phone. To start over, dial 0.")
        self.dial_callbacks = {
            "8": self.move_to_ouija_e,
            "0": self.start_ouija
        }

    def on_enter_ouija_e(self):
        self.dial_callbacks = {
            "3": self.move_to_ouija_a,
            "0": self.start_ouija
        }

    def on_enter_ouija_a(self):
        self.dial_callbacks = {
            "2": self.move_to_ouija_question_mark,
            "0": self.start_ouija
        }

    def on_enter_ouija_question_mark(self):
        print("Follow what the ghost tells you. To start again, dial 0.")
        self.dial_callbacks = {
            "0": self.start_ouija
        }

    def direct_to_book(self):
        print("Pls find your copy of Ghosthunting For Beginners; to hear this information again, please "
              "dial 1. Once you have found the name of your ghost, please dial 9.")

Hallowpuzz()

while True:
    time.sleep(1)
