from machine import Pin
from tm1650 import TM1650
from keypad import Keypad
from time import sleep

# Define GPIO pins for rows
row_pins = [Pin(15),Pin(12),Pin(13),Pin(14)]

# Define GPIO pins for columns
column_pins = [Pin(2),Pin(3),Pin(4)]

# Define keypad layout
keys = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#']]

keypad = Keypad(row_pins, column_pins, keys)

SDA_PIN = 0
SCL_PIN = 1
disp = TM1650(SDA_PIN, SCL_PIN)

disp.display_on()
disp.display_clear()

s = ""

while True:
    key_pressed = keypad.read_keypad()
    if key_pressed:
        print("Key pressed:", key_pressed)
        s = (s + key_pressed)[-4:]
        disp.display_string(s)
    sleep(0.2)  # debounce and delay

def scroll_string(s):
  s = s.upper()
  doublemsg = s + s
  for i in range(len(s) - 3):
    disp.display_string(doublemsg[i:4+i])
    sleep(0.4)

def scroll_infinitely(s):
  s = s.upper()
  doublemsg = s + "    " + s
  i = 0
  while True:
    disp.display_string(doublemsg[i:4+i])
    sleep(0.2)
    i = (i + 1) % (len(s) + 4)

scroll_infinitely("clippy is dead?!")

while True:
    scroll_string("out of order")
    disp.display_clear()
    sleep(1)

for i in range(10000):
  disp.display_integer(i)

disp.display_clear()
disp.display_off()
