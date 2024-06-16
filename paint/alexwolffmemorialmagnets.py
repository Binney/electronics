from gpiozero import Button, LED

pencil = Button(2)

print("HEREWEGOOOO")
state = True
while True:
    if pencil.is_pressed:
        if not state:
            state = True
            print("on!")
    else:
        if state:
            state = False
            print("Off!")

