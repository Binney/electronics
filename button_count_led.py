print("Hello world!")

from adafruit_circuitplayground import cp
import time
import rainbowio
from audiopwmio import PWMAudioOut as AudioOut
import audiocore
import math
import board
import digitalio

brown = digitalio.DigitalInOut(board.A3)
orange = digitalio.DigitalInOut(board.A2)

def beep_times(num):
    print("I beep this many times:")
    print(num)
    cp.pixels.fill((0,0,0))
    cp.pixels[num % 10] = (0,30,5)

button_state = False
counter = 0

while True:
    dialling = brown.value
    if not dialling:
        if counter > 0:
            print("Finished with non-zero value for counter")
            print(counter)
            beep_times(counter)
            counter = 0
    else:
        if orange.value:
            cp.red_led = True
            if button_state:
                # Was on, stay on
                pass
            else:
                # Was off, now on
                print("Yes on!")
            button_state = True
        else:
            cp.red_led = False
            if button_state:
                # Was on, now off
                print("Now off!")
                counter += 1
                pass
            else:
                # Was off, stay off
                pass
            button_state = False
