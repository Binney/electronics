from time import sleep
import board
import busio
from adafruit_ht16k33.segments import Seg7x4

i2c = busio.I2C(board.GP27, board.GP26)
display = Seg7x4(i2c)
display.print("9999")
sleep(5)

while True:
    display.print("HELL")
    sleep(0.5)
    display.print("ELL0")
    sleep(0.5)
    display.print("LL0 ")
    sleep(0.5)
    display.print("L0  ")
    sleep(0.5)
    display.print("0   ")
    sleep(0.5)
    display.print("   H")
    sleep(0.5)
    display.print("  HE")
    sleep(0.5)
    display.print(" HEL")
    sleep(0.5)
