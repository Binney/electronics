print("ok letsgoooooo")

import time
import board
import digitalio

builtinled = digitalio.DigitalInOut(board.LED)
builtinled.direction = digitalio.Direction.OUTPUT

led = digitalio.DigitalInOut(board.GP14)
led.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.GP13)
button.switch_to_input(pull=digitalio.Pull.DOWN)

led.value = True
time.sleep(0.5)
led.value = False

while True:
    if button.value:
        led.value = True
        builtinled.value = True
        print("Yes on!")
    led.value = False
    builtinled.value = False
#    time.sleep(0.2)
#    led.value = False
#    builtinled.value = False
#    time.sleep(0.2)
