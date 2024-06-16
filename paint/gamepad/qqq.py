# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# You must add a gamepad HID device inside your boot.py file
# in order to use this example.
# See this Learn Guide for details:
# https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/hid-devices#custom-hid-devices-3096614-9

import board
import digitalio
import analogio
import usb_hid

from hid_gamepad import Gamepad

gp = Gamepad(usb_hid.devices)

# Create some buttons. The physical buttons are connected
# to ground on one side and these and these pins on the other.
button_pins = (board.GP6, board.GP7, board.GP8, board.GP9)

# Map the buttons to button numbers on the Gamepad.
# gamepad_buttons[i] will send that button number when buttons[i]
# is pushed.
gamepad_buttons = (13, 14, 15, 16)

buttons = [digitalio.DigitalInOut(pin) for pin in button_pins]
for button in buttons:
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP


while True:
    # Buttons are grounded when pressed (.value = False).
    for i, button in enumerate(buttons):
        gamepad_button_num = gamepad_buttons[i]
        if button.value:
            gp.release_buttons(gamepad_button_num)
            # print(" release", gamepad_button_num, end="")
        else:
            gp.press_buttons(gamepad_button_num)
            # print(" press", gamepad_button_num, end="")


