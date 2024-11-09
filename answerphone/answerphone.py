from pyaudio import PyAudio, paInt16, paFloat32
import wave
import time
import keyboard
import atexit
from os import listdir
import random
import numpy as np

p = PyAudio()
def terminate():
    p.terminate()
atexit.register(terminate)

chunk = 4096
sample_format = paInt16
channels = 1
fs = 44100
max_recording_length = 5 * 60

sine_duration = 0.05
f = 220
samples = (np.sin(2 * np.pi * np.arange(fs * sine_duration) * f  / fs)).astype(np.float32)
output_bytes = (0.5 * samples).tobytes()

def play_tone():
    print("Playing tone")
    stream = p.open(format=paFloat32,
                    channels=channels,
                    rate=fs,
                    output=True)
    while True:
        if keyboard.is_pressed("q"):
            # Start recording
            stream.stop_stream()
            stream.close()
            take_recording()
            return
        if keyboard.is_pressed("c") or keyboard.is_pressed("z"):
            break
        stream.write(output_bytes)
    stream.stop_stream()
    stream.close()
    time.sleep(0.1)

def save_wave(frames):
    filename = "recordings/recording_" + str(time.time()) + ".wav"
    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

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

    print("Recording")

    stream = p.open(format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk, input=True)

    frames = []

    for i in range(0, int(fs / chunk * max_recording_length)):
        if keyboard.is_pressed('z') or keyboard.is_pressed("c"):
            print("stopp")
            break
        data = stream.read(chunk)
        frames.append(data)

    print("Stopping recording")

    stream.stop_stream()
    stream.close()

    save_wave(frames)

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

print("Hello world!")
print("Dial 1 to start recording...")

while True:
    if keyboard.is_pressed("x"):
        # Took phone off hook
        # Wait for dial
        play_tone()
    if keyboard.is_pressed("q"):
        take_recording()
    elif keyboard.is_pressed("w"):
        play_instructions_en()
    elif keyboard.is_pressed("e"):
        play_instructions_ro()
    elif keyboard.is_pressed("r"):
        play_instructions_es()
    elif keyboard.is_pressed("t"):
        play_random()

