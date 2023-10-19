import time

import keyboard_input_emulators

qq_a_meme = ""

class Hallowphone:
    def __init__(self):

        self.dial_history = ""
        self.dial_callbacks = {}
        self.init_phone_tree()
        keyboard_input_emulators.set_up_keyboard_phone_emulator(self.dialled_digit, self.off_hook)
        keyboard_input_emulators.set_up_keyboard_door_emulator(self.door_opened)

    def play_intro(self):
        print("To access the Ghost Detection Service, please press 1")

    def play_other(self):
        print("QQ a meme")

    def init_phone_tree(self):
        self.dial_callbacks = {
            "1": self.play_intro,
            "234": self.play_other
        }

    def off_hook(self):
        print("Phone off hook")

    def door_opened(self):
        print("Door opened")

    def dialled_digit(self, digit):
        self.dial_history += str(digit)
        print(self.dial_history)
        callback = next((callback for sequence, callback in self.dial_callbacks.items() if self.dial_history.endswith(sequence)), None)
        if callback:
            self.dial_history = ""
            callback()

Hallowphone()

while True:
    time.sleep(1)
