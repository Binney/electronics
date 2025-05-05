from time import sleep
import board
import busio
from adafruit_ht16k33.segments import Seg7x4
from random import random, randrange
from analogio import AnalogIn

pot = AnalogIn(board.GP28)

i2c = busio.I2C(board.GP27, board.GP26)
display = Seg7x4(i2c)
display.print("8888")
sleep(1)
display.print("    ")
sleep(0.5)

for i in range(4):
    for j in range(50):
        rand = randrange(0, 10 ** (i + 1))
        display.print(f"{rand:>4}")
        sleep(0.05)

while True:
    reading = pot.value
    offset = randrange(0, 10)
    normalised_reading = reading * 10000 / 65535 + offset
    normalised_reading = max(0, min(9999, normalised_reading))
    display.print(f"{int(normalised_reading):04}")
    sleep(0.05)
