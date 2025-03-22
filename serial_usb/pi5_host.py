# You will need to enable Serial before this will work
# sudo raspi-config
# Interface Options -> Serial
# Would you like a login shell to be accessible over serial? -> doesn't matter, I had it on
# Would you like the serial port hardware to be enabled? -> Yes
# Reboot

from serial import Serial
import time

class ConnectedPico:
    def __init__(self, port):
        self.port = port
        self.serial = Serial(port, 9600) # The baud rate technically doesn't matter here https://github.com/orgs/micropython/discussions/9619

    def send(self, message):
        # be sure to include the `\n` at the end of your messages as the device is doing a readline!
        self.serial.write(f"{self.port} > {message}\n")

pico0 = ConnectedPico("/dev/ttyACM0")
pico1 = ConnectedPico("/dev/ttyACM1")

while True:
    print("sending")
    pico0.send("Hello!")
    time.sleep(1)
    pico1.send("Hi!")
    time.sleep(1)
