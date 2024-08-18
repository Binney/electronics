from pyaudio import PyAudio, paInt16
import wave

print("Hello world!")
p = PyAudio()

for ii in range(p.get_device_count()):
    print(p.get_device_info_by_index(ii))

chunk = 1024
sample_format = paInt16
channels = 2
fs = 44100
max_recording_length = 5
filename = "output.wav"

print("Recording")

stream = p.open(format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk, input=True)

frames = []

try:
    for i in range(0, int(fs / chunk * max_recording_length)):
        data = stream.read(chunk)
        frames.append(data)
except KeyboardInterrupt:
    pass

print("Stopping recording")

stream.stop_stream()
stream.close()

p.terminate()

wf = wave.open(filename, "wb")
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()
