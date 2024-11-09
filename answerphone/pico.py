import math
import time
import digitalio
import board
from adafruit_debouncer import Debouncer
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode


class RotaryPhoneInput():
    def __init__(self, keypress_callback):
        self.pulses = 0
        self.counting = False
        self.keypress_callback = keypress_callback

        # Red
        pin_dial_pulser = digitalio.DigitalInOut(board.GP22)
        pin_dial_pulser.direction = digitalio.Direction.INPUT
        pin_dial_pulser.pull = digitalio.Pull.UP
        self.dial_pulser = Debouncer(pin_dial_pulser)

        # Blue
        pin_dialling = digitalio.DigitalInOut(board.GP16)
        pin_dialling.direction = digitalio.Direction.INPUT
        pin_dialling.pull = digitalio.Pull.UP
        self.dialling = Debouncer(pin_dialling)

        # Yellow
        pin_hook = digitalio.DigitalInOut(board.GP15)
        pin_hook.direction = digitalio.Direction.INPUT
        pin_hook.pull = digitalio.Pull.UP
        self.hook = Debouncer(pin_hook)

    def start_counting(self):
        if self.off_hook():
            print("Start counting")
            self.keypress_callback(Keycode.C)
            self.counting = True
        else:
            print("Not counting; phone on hook")

    def stop_counting(self):
        if self.counting:
            print("Stop counting; pulses: " + str(self.pulses))
            self.counting = False

            if self.pulses % 2 != 0:
                print("Got odd number of pulses: " + str(self.pulses))
            if self.pulses > 0:
                digit = None
                if math.floor(self.pulses / 2) == 10:
                    digit = 0
                else:
                    digit = math.floor(self.pulses / 2)
                self.pulses = 0

                print("Received digit: " + str(digit))
                key_to_send = self.map_digit_to_keypress(digit)
                self.keypress_callback(key_to_send)

    def add_pulse(self):
        if self.counting:
            self.pulses += 1
            print("Add pulse: " + str(self.pulses))

    def off_hook(self):
        return not self.hook.value

    def reset(self):
        self.pulses = 0

    def tick(self):
        self.hook.update()
        if self.hook.rose:
            print("Replaced on hook")
            self.keypress_callback(Keycode.Z)
        if self.hook.fell:
            print("Lifted from hook")
            self.keypress_callback(Keycode.X)
        self.dial_pulser.update()
        if self.dial_pulser.fell or self.dial_pulser.rose:
            self.add_pulse()
        self.dialling.update()
        if self.dialling.fell:
            self.start_counting()
        elif self.dialling.rose:
            self.stop_counting()

    def debug(self):
        print("Dialling: " + str(self.dialling.value) +
              "  ::  Pulser: " + str(self.dial_pulser.value) +
              "  ::  On hook: " + str(self.hook.value))
        time.sleep(0.5)

    @staticmethod
    def map_digit_to_keypress(digit):
        if digit == 1:
            return Keycode.Q
        elif digit == 2:
            return Keycode.W
        elif digit == 3:
            return Keycode.E
        elif digit == 4:
            return Keycode.R
        elif digit == 5:
            return Keycode.T
        elif digit == 6:
            return Keycode.Y
        elif digit == 7:
            return Keycode.U
        elif digit == 8:
            return Keycode.I
        elif digit == 9:
            return Keycode.O
        elif digit == 0:
            return Keycode.P


class KeyboardHIDOutput():
    def __init__(self):
        self.keyboard = Keyboard(usb_hid.devices)

    def send_keypress(self, key):
        print("Sending keypress: " + str(key))
        self.keyboard.press(key)
        time.sleep(0.1)
        self.keyboard.release(key)


keyboard_output = KeyboardHIDOutput()
phone_input = RotaryPhoneInput(keyboard_output.send_keypress)

print("Keyboard running")

while True:
    phone_input.tick()
    #phone_input.debug()
