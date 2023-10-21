import math

import gpiozero

# Binneyphone

pin_dialling = 19  # yellow on pi; brown in phone
pin_dial_pulser = 13  # blue on pi; orange in phone
pin_on_hook = 26  # red on pi; yellow in phone
# Ground: Black on pi; grey from hook and red from dialler in phone


dialling = gpiozero.DigitalInputDevice(pin_dialling, pull_up=True, bounce_time=None)
dial_pulser = gpiozero.DigitalInputDevice(pin_dial_pulser, pull_up=True, bounce_time=None)
on_hook = gpiozero.DigitalInputDevice(pin_on_hook, pull_up=True, bounce_time=None)


class Dial():
    def __init__(self, digit_callback):
        self.pulses = 0
        self.counting = True
        self.digit_callback = digit_callback

    def start_counting(self):
        print("Start counting")
        self.counting = True

    def stop_counting(self):
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

            self.digit_callback(digit)

    def add_pulse(self):
        print("Add pulse")
        if self.counting:
            self.pulses += 1
            print(self.pulses)

    def reset(self):
        self.pulses = 0


def set_up_phone_input(digit_callback, off_hook_callback):
    dial = Dial(digit_callback)

    dial_pulser.when_deactivated = dial.add_pulse
    dial_pulser.when_activated = dial.add_pulse
    dialling.when_activated = dial.start_counting
    dialling.when_deactivated = dial.stop_counting
    on_hook.when_deactivated = off_hook_callback
