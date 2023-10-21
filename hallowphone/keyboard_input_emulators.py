import keyboard


def set_up_keyboard_phone_emulator(digit_callback, off_hook_callback):
    def on_key_press(event):
        if "0" <= event.name <= "9":
            digit_callback(int(event.name))
        elif event.name == "space":
            off_hook_callback()

    keyboard.on_press(on_key_press)


def set_up_keyboard_door_emulator(door_opened_callback):
    def on_key_press(event):
        if event.name == "enter":
            door_opened_callback()

    keyboard.on_press(on_key_press)
