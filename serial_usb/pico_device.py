# Assumes CircuitPython
# If you're using MicroPython, this penguin has you covered: https://www.youtube.com/watch?v=egOOW0WstRg

import time
import board
import digitalio
import select
import sys
import usb_cdc

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

def read_serial(serial):
    text = ""
    available = serial.in_waiting
    while available:
        raw = serial.read(available)
        text = raw.decode("utf-8")
        available = serial.in_waiting
    return text

def wait_for_handshake():
    buffer = ""
    serial = usb_cdc.console
    while True:
        time.sleep(0.01)
        print("My name is: fish")
        buffer += read_serial(serial)
        if buffer.endswith("Acknowledge: fish!\n"):
            print("Ready to go!")
            return

wait_for_handshake()

print("reading")
while True:
    if select.select([sys.stdin], [], [], 0)[0]:
        led.value = True
        data = sys.stdin.readline()
        print(data)
        time.sleep(0.5) # just enough you can see the light, remove if you don't need it
        led.value = False
