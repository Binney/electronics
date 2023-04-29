print("Hello world!")

from time import sleep
import math
from gpiozero import Button, LED
import vlc

dialling = Button(17) # brown
dial_pulser = Button(27) # orange
off_hook = Button(22) # yellow

indicator = LED(23)

num_dialled = ''

button_state = False
counter = 0

playing = False

ringing = vlc.MediaPlayer("file:///home/sarbin/Documents/ringing.mp3")
success = vlc.MediaPlayer("file:///home/sarbin/Documents/dialup.mp3")

while True:
    if off_hook.is_pressed:
        if not playing:
            ringing.play()
            playing = True
    else:
        ringing.stop()
        playing = False

        if dialling.is_pressed:
            if dial_pulser.is_pressed:
                indicator.on()
                if button_state:
                    # Was on, stay on
                    pass
                else:
                    # Was off, now on
                    print("Yes on!")
                    counter += 1
                button_state = True
            else:
                indicator.off()
                if button_state:
                    # Was on, now off
                    print("Now off!")
                    pass
                else:
                    # Was off, stay off
                    pass
                button_state = False
        else:
            if counter > 0:
                print("Adding number to what dialled:")
                print(counter)
                num_dialled += str(counter % 10)
                print("Brings us up to:")
                print(num_dialled)
                counter = 0
        
                if len(num_dialled) == 3:
                    if num_dialled == '123':
                        print("That's correct!")
                        success.play()
                    else:
                        print("Nope, wrong")
                    num_dialled = ''
