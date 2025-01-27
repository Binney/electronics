from time import sleep
import board
import busio
from adafruit_ht16k33.segments import Seg7x4

i2c = busio.I2C(board.GP27, board.GP26)
display = Seg7x4(i2c)
display.print("9999")
sleep(1)
display.print("    ")
sleep(0.5)

while True:
    message = "HELL0 ALL   "
    doublemsg = message + message
    for i in range(len(message)):
        display.print(doublemsg[i:4+i])
        sleep(0.5)
