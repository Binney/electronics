import math
import time
import digitalio
import board
from adafruit_debouncer import Debouncer
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode


class RotaryPhoneInput():
    def __init__(self, digit_callback):
        self.pulses = 0
        self.counting = False
        self.digit_callback = digit_callback

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
        self.pin_hook = digitalio.DigitalInOut(board.GP15)
        self.pin_hook.direction = digitalio.Direction.INPUT
        self.pin_hook.pull = digitalio.Pull.UP

    def start_counting(self):
        if self.off_hook():
            print("Start counting")
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
                self.digit_callback(digit)

    def add_pulse(self):
        if self.counting:
            self.pulses += 1
            print("Add pulse: " + str(self.pulses))

    def off_hook(self):
        return not self.pin_hook.value

    def reset(self):
        self.pulses = 0

    def tick(self):
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
              "  ::  On hook: " + str(self.pin_hook.value))
        time.sleep(0.5)


class KeyboardHIDOutput():
    def __init__(self):
        self.keyboard = Keyboard(usb_hid.devices)

    def send_keypress_for_digit(self, digit):
        print("Sending keypress for digit: " + str(digit))
        self.keyboard.send(self.map_digit_to_keypress(digit))

    @staticmethod
    def map_digit_to_keypress(digit):
        if digit == 1:
            return Keycode.ONE
        elif digit == 2:
            return Keycode.TWO
        elif digit == 3:
            return Keycode.THREE
        elif digit == 4:
            return Keycode.FOUR
        elif digit == 5:
            return Keycode.FIVE
        elif digit == 6:
            return Keycode.SIX
        elif digit == 7:
            return Keycode.SEVEN
        elif digit == 8:
            return Keycode.EIGHT
        elif digit == 9:
            return Keycode.NINE
        elif digit == 0:
            return Keycode.ZERO


keyboard_output = KeyboardHIDOutput()
phone_input = RotaryPhoneInput(keyboard_output.send_keypress_for_digit)

print("Keyboard running")

while True:
    phone_input.tick()
    # Uncomment me to debug which pins are connected:
    #phone_input.debug()
