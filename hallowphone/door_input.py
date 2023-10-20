import gpiozero

pin_door_closed = 26  # red
door_closed = gpiozero.DigitalInputDevice(pin_door_closed, pull_up=True, bounce_time=None)


def set_up_door_input(door_opened_callback):
    door_closed.when_deactivated = door_opened_callback
