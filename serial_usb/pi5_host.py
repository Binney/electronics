# You will need to enable Serial before this will work
# sudo raspi-config
# Interface Options -> Serial
# Would you like a login shell to be accessible over serial? -> doesn't matter, I had it on
# Would you like the serial port hardware to be enabled? -> Yes
# Reboot

from serial import Serial
from serial.tools.list_ports import comports
import time

class ConnectedPico:
    def __init__(self, port):
        self.port = port
        self.serial = Serial(port, 9600) # The baud rate technically doesn't matter here https://github.com/orgs/micropython/discussions/9619
        self.name = "unknown"

    def set_name(self, name):
        self.name = name

    def send(self, message):
        # be sure to include the `\n` at the end of your messages as the device is doing a readline!
        self.serial.write(f"{self.port} > {message}\n")

    def read(self):
        return self.serial.read_until()

def get_connected_devices():
    result = []
    for port in comports():
        print(port.device)
        if (port.device.startswith("/dev/ttyACM")):
            result.append(port.device)
    return result

ports = get_connected_devices()
print(ports)

picos = []
for port in ports:
    print(f"Connecting to {port}")
    pico = ConnectedPico(port)
    handshake = pico.read() # TODO: make this ignore the start and end bytes e.g. prompt
    print(f"Made a handshake: {handshake}")
    pico.set_name(handshake)
    picos.append(pico)

while True:
    print("loop start")
    for pico in picos:
        if pico.name == "I am pico #0":
            pico.send("action for 0")
        elif pico.name == "I am pico #1":
            pico.send("action for 1")
        else:
            pico.send("action for unknown pico")
    time.sleep(2)
