print("Hello world!")

from adafruit_circuitplayground import cp
import time
import rainbowio
from audiopwmio import PWMAudioOut as AudioOut
import audiocore
import math
import board
import digitalio

dialling = digitalio.DigitalInOut(board.A3) # brown
dial_pulser = digitalio.DigitalInOut(board.A2) # orange
off_hook = digitalio.DigitalInOut(board.A1) # yellow

num_dialled = ''

button_state = False
counter = 0

audio = AudioOut(board.AUDIO)
wave_file = None

def play_wav(name, loop=False):
    """
    Play a WAV file in the 'sounds' directory.
    :param name: partial file name string, complete name will be built around
                 this, e.g. passing 'foo' will play file 'sounds/foo.wav'.
    :param loop: if True, sound will repeat indefinitely (until interrupted
                 by another sound).
    """
    global wave_file  # pylint: disable=global-statement
    print("playing", name)
    if wave_file:
        wave_file.close()
    try:
        wave_file = open('sounds/' + name + '.wav', 'rb') # using wave files from sounds folder
        wave = audiocore.WaveFile(wave_file)
        audio.play(wave, loop=loop)
    except OSError:
        pass # we'll just skip playing then

while True:
    if off_hook.value:
        if not audio.playing:
            play_wav('telephone', True)
    else:
        audio.stop()
        cp.stop_tone()

        if dialling.value:
            if dial_pulser.value:
                cp.red_led = True
                if button_state:
                    # Was on, stay on
                    pass
                else:
                    # Was off, now on
                    print("Yes on!")
                    counter += 1
                button_state = True
            else:
                cp.red_led = False
                if button_state:
                    # Was on, now off
                    print("Now off!")
                    pass
                else:
                    # Was off, stay off
                    pass
                button_state = False
        else:
            # qq this bit's speculative as `audio` ain't working :'(
            cp.start_tone(440)
            if counter > 0:
                print("Adding number to what dialled:")
                print(counter)
                cp.pixels.fill((0,0,0))
                cp.pixels[counter % 10] = (0,30,5)
                num_dialled += str(counter)
                print("Brings us up to:")
                print(num_dialled)
                counter = 0

                if len(num_dialled) == 5:
                    if num_dialled == '12345':
                        print("That's correct!")
                    else:
                        print("Nope, wrong")
                    num_dialled = ''

