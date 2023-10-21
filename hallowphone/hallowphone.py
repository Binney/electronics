import time
from pathlib import Path
import keyboard_input_emulators
import magnet_output_emulators
# import rotary_phone_input
# import door_input
# import magnets
from transitions import Machine
import logging
import os
import vlc

# Required on Windows; comment out on Pi
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')


logging.basicConfig(level=logging.INFO)
logging.getLogger('transitions').setLevel(logging.INFO)

vlc_ins = vlc.Instance()
player = vlc_ins.media_player_new()

sounds_directory = Path(__file__).parent / "sounds"
loud_ringing_sound = vlc_ins.media_new(sounds_directory / "loud_ringing_sound.mp3")
silly_ring_do_not_use = vlc_ins.media_new(sounds_directory / "silly_ring_do_not_use.m4a")
first_camden_council_call = vlc_ins.media_new(sounds_directory / "first_camden_council_call.m4a")
on_later_pick_off_hook = vlc_ins.media_new(sounds_directory / "on_later_pick_off_hook.m4a")
ghost_name_prompt = vlc_ins.media_new(sounds_directory / "ghost_name_prompt.m4a")
book_info = vlc_ins.media_new(sounds_directory / "book_info.m4a")
ouija_prompt = vlc_ins.media_new(sounds_directory / "ouija_prompt.m4a")
ouija_complete = vlc_ins.media_new(sounds_directory / "ouija_complete.m4a")
dial_zero = vlc_ins.media_new(sounds_directory / "dial_zero.m4a")
boo = vlc_ins.media_new(sounds_directory / "boo.m4a")


# noinspection PyUnresolvedReferences
class Hallowpuzz(object):
    states = ['initial', 'first_camden_message', 'searching_for_ghost_name', 'inputting_ghost_name', 'ouija_t',
              'ouija_e', 'ouija_a', 'ouija_question_mark']

    def __init__(self):
        self.dial_history = ""
        self.dial_callbacks = {}

        self.machine = Machine(model=self, states=Hallowpuzz.states, initial='initial')

        self.machine.add_transition(trigger='first_phone_pick_up',
                                    source='initial',
                                    dest='first_camden_message')
        self.machine.add_transition(trigger='move_to_search_for_ghost_name',
                                    source=['first_camden_message', 'inputting_ghost_name'],
                                    dest='searching_for_ghost_name')
        self.machine.add_transition(trigger='start_inputting_ghost_name',
                                    source='searching_for_ghost_name',
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
            self.play_sound(silly_ring_do_not_use)

    def off_hook(self):
        player.stop()
        print("Phone off hook")
        if self.is_initial():
            print("Playing first Camden council call")
            self.play_sound_with_delay(first_camden_council_call)
            self.first_phone_pick_up()
        elif self.is_first_camden_message():
            print("Playing first Camden council call")
            self.play_sound_with_delay(first_camden_council_call)
        elif self.is_searching_for_ghost_name():
            print("Playing repeat intro")
            self.play_sound_with_delay(on_later_pick_off_hook)
        elif self.is_inputting_ghost_name():
            self.move_to_search_for_ghost_name()
            print("Playing repeat intro")
            self.play_sound_with_delay(on_later_pick_off_hook)
        else:
            print("Playing restart info")
            self.play_sound_with_delay(dial_zero)

    def dialled_digit(self, digit):
        print("Received digit: " + str(digit))
        self.dial_history += str(digit)
        print("Dial history: " + self.dial_history)
        callback = next((
            callback for sequence, callback in self.dial_callbacks.items() if self.dial_history.endswith(sequence)),
            self.dial_callbacks.get("default"))
        if callback:
            self.dial_history = ""
            callback()

    def on_enter_first_camden_message(self):
        self.dial_callbacks = {
            "1": self.begin_search_for_ghost_name
        }

    def on_enter_searching_for_ghost_name(self):
        self.dial_callbacks = {
            "1": self.direct_to_book,
            "9": self.start_inputting_ghost_name
        }

    def on_enter_inputting_ghost_name(self):
        print("Playing ghost name prompt")
        self.play_sound(ghost_name_prompt)
        self.dial_callbacks = {
            "254779": self.start_ouija,
            "0": self.restart_search_for_ghost_name
        }

    def on_enter_ouija_t(self):
        print("Playing ouija prompt")
        self.play_sound(ouija_prompt)
        magnet_output_emulators.enable_t()
        self.dial_callbacks = {
            "8": self.move_to_ouija_e,
            "0": self.start_ouija,
            "default": self.start_ouija
        }

    def on_enter_ouija_e(self):
        print("Playing boo")
        self.play_sound(boo)
        magnet_output_emulators.enable_e()
        self.dial_callbacks = {
            "3": self.move_to_ouija_a,
            "0": self.start_ouija,
            "default": self.start_ouija
        }

    def on_enter_ouija_a(self):
        print("Playing boo")
        self.play_sound(boo)
        magnet_output_emulators.enable_a()
        self.dial_callbacks = {
            "2": self.move_to_ouija_question_mark,
            "0": self.start_ouija,
            "default": self.start_ouija
        }

    def on_enter_ouija_question_mark(self):
        print("Playing ouija complete")
        self.play_sound(ouija_complete)
        magnet_output_emulators.enable_question_mark()
        self.dial_callbacks = {
            "0": self.start_ouija
        }

    def direct_to_book(self):
        print("Playing book info")
        self.play_sound(book_info)

    def begin_search_for_ghost_name(self):
        self.direct_to_book()
        self.move_to_search_for_ghost_name()

    def restart_search_for_ghost_name(self):
        print("Playing repeat intro")
        self.play_sound_with_delay(on_later_pick_off_hook)
        self.move_to_search_for_ghost_name()

    def play_sound(self, sound):
        player.stop()
        player.set_media(sound)
        player.play()

    def play_sound_with_delay(self, sound):
        time.sleep(2)
        self.play_sound(sound)


Hallowpuzz()

while True:
    time.sleep(1)
