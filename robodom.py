from machine import ADC, Pin, Timer
from time import sleep

led = Pin(25, Pin.OUT)
btn = Pin(2, Pin.IN, Pin.PULL_UP)#Button(16)
timer = Timer()

led.on()
sleep(1)
led.off()

print("Hello world!")

white = Pin(6, Pin.OUT)
green = Pin(7, Pin.OUT)
red = Pin(8, Pin.OUT)

breathlyser = ADC(Pin(28))

def assess():
    print("Assess!")
    total = 0
    count = 0
    while count < 100:
        print(breathlyser.read_u16())
        if breathlyser.read_u16() > 30000:
            total += 1
        sleep(0.1)
        count += 1
    return total > 90

while True:
    led.value(btn.value())
    if not btn.value():
        white.on()
        result = assess()
        white.off()
        print("Dom thinks:")
        print(result)
        if result:
            green.on()
        else:
            red.on()
        sleep(1)
        green.off()
        red.off()
        while not btn.value():
            pass

