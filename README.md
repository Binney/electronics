# Electronics Tips

Here are some useful links and basic code snippets!

## Links

[Interactive Pi Pico Pinout](https://pico.pinout.xyz/)

[CircuitPython uf2 download](https://circuitpython.org/board/raspberry_pi_pico/)

[Adafruit CircuitPython library bundle](https://circuitpython.org/libraries) (you shouldn't need this if you're using the VS Code extension)

[VS Code](https://code.visualstudio.com/)

[CircuitPython v2 VS Code extension](https://marketplace.visualstudio.com/items?itemName=wmerkens.vscode-circuitpython-v2)

[My etch a sketch mouse tutorial](https://blog.dreamcat.uk/etch-a-sketch-mouse-with-raspberry-pi-pico)

[Adafruit HID tutorial](https://learn.adafruit.com/circuitpython-essentials/circuitpython-hid-keyboard-and-mouse)

[Adafruit HID docs and examples using mouse, keyboard and gamepad](https://docs.circuitpython.org/projects/hid/en/latest/examples.html)

[Custom HID descriptors](https://learn.adafruit.com/custom-hid-devices-in-circuitpython?view=all) (more complex)

## Pico setup

1. Download UF2 for the correct board (28th July: we are using Pi Pico, not W, not 2)
1. Plug Pico into your computer with a decent USB Micro cable.
1. Copy UF2 to root of device.
1. Open VS Code with extension installed.
1. CircuitPython: Select Serial Port -> click whatever it says
1. CircuitPython: Choose CircuitPython Board -> Raspberry Pi:Pico
1. CircuitPython: Open Serial Monitor
1. Install dependencies: CircuitPython: Show Available Libraries
1. Write code
1. Hack
1. Have fun!

## Sample code

### Blinky

```
import board
import digitalio
from time import sleep

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True
    sleep(1)
    led.value = False
    sleep(1)
```


### Pressy Buttony

```
import time
import board
from digitalio import DigitalInOut, Direction, Pull

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

switch = DigitalInOut(board.GP15)
switch.direction = Direction.INPUT
switch.pull = Pull.UP

while True:
    if switch.value:
        led.value = False
    else:
        led.value = True
    time.sleep(0.01)
```

### Debouncing

```
import board
import digitalio
from adafruit_debouncer import Debouncer

pin = digitalio.DigitalInOut(board.GP15)
pin.direction = digitalio.Direction.INPUT
pin.pull = digitalio.Pull.UP
switch = Debouncer(pin)

while True:
	switch.update()
	if switch.fell:
		print('Just pressed')
	if switch.rose:
		print('Just released')
```

### Basic keyboard

```
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from time import sleep

keyboard = Keyboard(usb_hid.devices)

while True:
    keyboard.send(Keycode.CAPS_LOCK)
    sleep(1)
```

### Separate press and release keyboard

```
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from time import sleep

keyboard = Keyboard(usb_hid.devices)

while True:
    keyboard.press(Keycode.CAPS_LOCK)
    sleep(0.5)
    keyboard.release(Keycode.CAPS_LOCK)
    sleep(1)
```
