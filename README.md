# Electronics Tips

Here are some useful links and basic code snippets!

## Links

[CircuitPython uf2 download](https://circuitpython.org/board/raspberry_pi_pico/)

[Adafruit CircuitPython library bundle](https://circuitpython.org/libraries) (you shouldn't need this if you're using the VS Code extension)

[VS Code](https://code.visualstudio.com/)

[CircuitPython v2 VS Code extension](https://marketplace.visualstudio.com/items?itemName=wmerkens.vscode-circuitpython-v2)


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

### Keyboard

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
