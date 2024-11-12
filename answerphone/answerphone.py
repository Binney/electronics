from pyaudio import PyAudio, paInt16, paContinue
import wave
import time
import keyboard
import atexit
from os import listdir
import random
from gpiozero import LED
import traceback
from datetime import datetime

p = PyAudio()
dial_tone = wave.open("tone.wav", "rb")

def terminate():
    dial_tone.close()
    p.terminate()
atexit.register(terminate)

chunk = 4096
sample_format = paInt16
channels = 1
fs = 44100
max_recording_length = 5 * 60

backup_external = True

led = LED(26)

for i in range(4):
    led.on()
    time.sleep(0.5)
    led.off()
    time.sleep(0.5)

def dial_tone_callback(in_data, frame_count, time_info, status):
    data = dial_tone.readframes(frame_count)
    if len(data) < frame_count * 4: # qq calculate this
        dial_tone.rewind()
        data = dial_tone.readframes(frame_count)
    return (data, paContinue)

def play_tone():
    time.sleep(0.1)
    print("Playing tone")

    dial_tone_stream = p.open(format=p.get_format_from_width(dial_tone.getsampwidth()),
                    channels=dial_tone.getnchannels(),
                    rate=dial_tone.getframerate(),
                    output=True,
                    stream_callback=dial_tone_callback)

    # Block until any key pressed
    ev = keyboard.read_event()
    print("Stopped tone")

    # This automatically stops calling the callback
    dial_tone_stream.stop_stream()
    dial_tone_stream.close()

def save_wave(filename, frames):
    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

def save_recording(frames):
    filename = "recording_" + datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S') + ".wav"
    print("Saving internal: " + filename)
    save_wave("recordings/" + filename, frames)
    if backup_external:
        print("Saving to SD card: " + filename)
        try:
            save_wave("/media/dreamcat/PHONEBACKUP/recordings/" + filename, frames)
        except:
            traceback.format_exc()
            print("Couldn't save file to SD card")


def play_wave(filename):
    wf = wave.open(filename, 'rb')

    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)

    data = wf.readframes(chunk)

    while data:
        if keyboard.is_pressed("z") or keyboard.is_pressed("c"):
            print("stopp")
            break
        stream.write(data)
        data = wf.readframes(chunk)

    wf.close()
    stream.close()

def take_recording():
    print("Play instructions")
    play_wave("instructions.wav")

    print("Recording")
    led.on()

    stream = p.open(format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk, input=True)

    frames = []

    for i in range(0, int(fs / chunk * max_recording_length)):
        if keyboard.is_pressed('z') or keyboard.is_pressed("c"):
            print("stopp")
            break
        data = stream.read(chunk)
        frames.append(data)

    print("Stopping recording")
    led.off()

    stream.stop_stream()
    stream.close()

    save_recording(frames)

def play_instructions_en():
    print("play English language instructions")
    play_wave("instructions.wav")

def play_instructions_ro():
    print("redati instructiuni în romana")
    play_wave("instructiuni.wav")

def play_instructions_es():
    print("reproducir las instrucciones en español")
    play_wave("instrucciones.wav")

def play_random():
    # This assumes the dir only has suitable wavs in. Please deal
    file = random.choice(listdir("./recordings"))
    print("Your random recording is:", file)
    play_wave("./recordings/" + file)

led.on()
time.sleep(1)
led.off()

print("Hello world!")
print("Dial 1 to start recording...")

while True:
    try:
        if keyboard.is_pressed("x"):
            # Took phone off hook
            # Wait for dial
            play_tone()
        if keyboard.is_pressed("q"):
            take_recording()
#    elif keyboard.is_pressed("w"):
#        play_instructions_en()
#    elif keyboard.is_pressed("e"):
#        play_instructions_ro()
#    elif keyboard.is_pressed("r"):
#        play_instructions_es()
#    elif keyboard.is_pressed("t"):
#        play_random()
    except KeyboardInterrupt:
        print("Byeeeeeeeee")
        break
    except:
        print(traceback.format_exc())
        print("Something went wrong. Oh well! Continue anyway")
        time.sleep(1)

