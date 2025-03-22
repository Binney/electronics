# Assumes CircuitPython
# If you're using MicroPython, this penguin has you covered: https://www.youtube.com/watch?v=egOOW0WstRg

import time
import board
import busio
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

uart = busio.uart(board.GP4, board.GP5, baudrate=115200, timeout=0)

while True:
    data = uart.read(1)
    if data is None:
        led.value = False
    else:
        print(data)
        led.value = True
