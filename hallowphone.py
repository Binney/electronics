print("Hello world!")

from time import sleep
import math
from gpiozero import Button, LED
import vlc
from pathlib import Path

dial_pulser = Button(13) # blue on pi; orange in phone
dialling = Button(19) # yellow on pi; brown in phone
off_hook = Button(26) # red on pi; yellow in phone
# Ground: Black on pi; greu from hook and red from dialler in phone

history = ""

##dialling = Button(17) # brown from phone
##dial_pulser = Button(27) # orange from phone
##off_hook = Button(22) # yellow from phone
## black wires to ground

vlc_ins = vlc.Instance()
player = vlc_ins.media_player_new()

sounds_directory = Path(__file__).parent / "public/sounds"
intro = vlc_ins.media_new(sounds_directory / "dialup-2a.mp3")
on_getting_matryoska = vlc_ins.media_new(sounds_directory / "dialup-3a.mp3")
on_getting_strangerlights = vlc_ins.media_new(sounds_directory / "dialup-6a.mp3")
on_getting_ouija = vlc_ins.media_new(sounds_directory / "dialup-7a.mp3")
# qq sounds

indicator = LED(23)

playing = False

def wait_for_dial():
    counter = 0
    button_state = True
    ticks_counter = 0

    while True:
        #sleep(0.1)
        #print(str(dialling.is_pressed) + " " + str(dial_pulser.is_pressed) + ' ' + str(off_hook.is_pressed))
        if not off_hook.is_pressed:
            pass
        else:
            if dialling.is_pressed:
                if player.is_playing():
                    player.pause()
                if dial_pulser.is_pressed:
                    indicator.on()
                    if button_state:
                        # Was on, stay on
                        ticks_counter += 1
                    else:
                        if ticks_counter < 100:
                            print("Was about to get a false ON; ticks count: " + str(ticks_counter))
                            pass
                        else:
                            # Was off, now on
                            counter += 1
                            print("== OFF TICKS: " + str(ticks_counter))
                            print("Is now on; incrementing keys to: " + str(counter))
                            ticks_counter = 0
                            button_state = True
                else:
                    indicator.off()
                    if button_state:
                        if ticks_counter < 100:
                            print("Was about to get a false OFF; ticks count: " + str(ticks_counter))
                            pass
                        else:
                            # Was on, now off
                            print("== ON TICKS: " + str(ticks_counter))
                            print("Now off!")
                            ticks_counter = 0
                            button_state = False
                    else:
                        # Was off, stay off
                        ticks_counter += 1
            else:
                if counter > 0:
                    print("You just dialled:")
                    print(counter)
                    
                    if counter > 10:
                        print("we should not be here :(((")

                    return counter % 10

while True:
    result = wait_for_dial()
    history += str(result)
    if len(history) > 20: # let's be reasonable now
        history = history[-20:]
    print("Dialled " + history)
    if history.endswith("999"):
        print("WOOOP WOOP")
