from adafruit_circuitplayground import cp
import time
import board
import busio
import digitalio

button_blue = digitalio.DigitalInOut(board.A5)
button_blue.switch_to_input(pull=digitalio.Pull.DOWN)
blue_pressed = False

button_red = digitalio.DigitalInOut(board.A2)
button_red.switch_to_input(pull=digitalio.Pull.DOWN)
red_pressed = False

button_green = digitalio.DigitalInOut(board.A3)
button_green.switch_to_input(pull=digitalio.Pull.DOWN)
green_pressed = False

button_yellow = digitalio.DigitalInOut(board.A1)
button_yellow.switch_to_input(pull=digitalio.Pull.DOWN)
yellow_pressed = False

def colour_pick(colour):
    print("{ 'action': 'colour_select', 'colour': '" + colour + "' }")

while True:
    if button_blue.value:
        cp.pixels[1] = (0, 30, 100)
        if not blue_pressed:
            colour_pick("blue")
            blue_pressed = True
    else:
        cp.pixels[1] = (0, 0, 0)
        blue_pressed = False

    if button_red.value:
        cp.pixels[2] = (100, 0, 0)
        if not red_pressed:
            colour_pick("red")
            red_pressed = True
    else:
        cp.pixels[2] = (0, 0, 0)
        red_pressed = False

    if button_green.value:
        cp.pixels[3] = (10, 100, 0)
        if not green_pressed:
            colour_pick("green")
            green_pressed = True
    else:
        cp.pixels[3] = (0, 0, 0)
        green_pressed = False

    if button_yellow.value:
        cp.pixels[4] = (100, 30, 0)
        if not yellow_pressed:
            colour_pick("yellow")
            yellow_pressed = True
    else:
        cp.pixels[4] = (0, 0, 0)
        yellow_pressed = False

