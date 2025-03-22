# You will need to enable Serial before this will work
# sudo raspi-config
# Interface Options -> Serial
# Would you like a login shell to be accessible over serial? -> doesn't matter, I had it on
# Would you like the serial port hardware to be enabled? -> Yes
# Reboot

from serial import Serial
import time

ser = Serial('/dev/ttyAMA0', 115200)

while True:
    print("sending")
    ser.write(str.encode("hello world"))
    time.sleep(5)
