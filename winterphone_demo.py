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

num_dialled = ''

button_state = False
counter = 0

while True:
    dialling = brown.value
    if dialling:
        if orange.value:
            cp.red_led = True
            if button_state:
                # Was on, stay on
                pass
            else:
                # Was off, now on
                print("Yes on!")
                #counter += 1
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
    else:
        if counter > 0:
            print("Now dialling:")
            print(counter)
            cp.pixels.fill((0,0,0))
            cp.pixels[counter % 10] = (0,30,5)
            num_dialled += str(counter)
            print("Brings us up to:")
            print(num_dialled)
            if len(num_dialled) == 5:
                if num_dialled == '12345':
                    print("That's correct!")
                else:
                    print("Nope, wrong")
                num_dialled = ''
            counter = 0

