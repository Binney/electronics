# Assumes CircuitPython
# If you're using MicroPython, this penguin has you covered: https://www.youtube.com/watch?v=egOOW0WstRg

import time
import board
import digitalio
import select
import sys

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

print("reading")
while True:
    if select.select([sys.stdin], [], [], 0)[0]:
        led.value = True
        data = sys.stdin.readline()
        print(data)
        time.sleep(0.5) # just enough you can see the light, remove if you don't need it
        led.value = False
