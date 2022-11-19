print("ok letsgoooooo")

import time
import board
import digitalio

clock = 0

builtinled = digitalio.DigitalInOut(board.LED)
builtinled.direction = digitalio.Direction.OUTPUT

led = digitalio.DigitalInOut(board.GP14)
led.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.GP13)
button.switch_to_input(pull=digitalio.Pull.DOWN)

led.value = True
time.sleep(0.5)
led.value = False

button_state = False
counter = 0

def beep_times(n):
    print("I beep this many times:")
    print(n)
    for i in range(n):
        led.value = True
        time.sleep(0.3)
        led.value = False
        time.sleep(0.3)

while True:
    if button.value:
        builtinled.value = True
        if button_state:
            # Was on, stay on
            pass
        else:   
            # Was off, now on
            button_state = True
            print("Yes on!")
            counter += 1
    else:
        builtinled.value = False
        if button_state:
            # Was on, now off
            clock = time.monotonic() # Start timeout to playback
            button_state = False
            print("Now off")
        else:
            # Was off, still off
            current_time = time.monotonic()
            if clock != 0 and current_time - clock >= 2:
                beep_times(counter)
                counter = 0
                clock = 0
