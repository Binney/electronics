import digitalio
import board
import usb_hid
from adafruit_hid.mouse import Mouse
import rotaryio

encoderL = rotaryio.IncrementalEncoder(board.GP19, board.GP18)
last_position_L = 0
buttonL = digitalio.DigitalInOut(board.GP17)
buttonL.direction = digitalio.Direction.INPUT
buttonL.pull = digitalio.Pull.UP
buttonL_state = None

encoderR = rotaryio.IncrementalEncoder(board.GP3, board.GP4)
last_position_R = 0
buttonR = digitalio.DigitalInOut(board.GP12)
buttonR.direction = digitalio.Direction.INPUT
buttonR.pull = digitalio.Pull.UP
buttonR_state = None

mouse = Mouse(usb_hid.devices)

led = digitalio.DigitalInOut(board.GP15)
led.direction = digitalio.Direction.OUTPUT
led.value = True

print("start!")

while True:
    position = encoderL.position
    if last_position_L != position:
        print("L: " + str(position))
        mouse.move((position - last_position_L) * -10, 0, 0)
    last_position_L = position

    position = encoderR.position
    if last_position_R != position:
        print("R: " + str(position))
        mouse.move(0, (position - last_position_R) * -10, 0)
    last_position_R = position

    if not buttonL.value and buttonL_state is None:
        buttonL_state = "pressed"
        mouse.press(1)
    if buttonL.value and buttonL_state == "pressed":
        mouse.release(1)
        buttonL_state = None

    if not buttonR.value and buttonR_state is None:
        buttonR_state = "pressed"
        mouse.press(2)
    if buttonR.value and buttonR_state == "pressed":
        mouse.release(2)
        buttonR_state = None
