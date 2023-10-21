from gpiozero import LED
from time import sleep
import random

G = LED(4)
H = LED(17)
O = LED(27)
S = LED(22)
T = LED(5)
I = LED(6)
D = LED(13)
C = LED(19)
L = LED(26)
U = LED(20)
E = LED(21)

all_leds = [G, H, O, S, T, I, D, C, L, U, E]
answer = [G, O, O, U, T, S, I, D, E, D, I, G]

while True:
    for led in answer:
        led.on()
        sleep(0.2)
        led.off()
        sleep(0.1)

    # all blink complete sequence
    for i in range(5):
        for led in all_leds:
            led.on()
        sleep(1 / ((i + 1) ** 2))
        for led in all_leds:
            led.off()

    sleep(5)

    shuffled_leds = all_leds.copy()
    shuffled_leds.extend(all_leds)
    shuffled_leds.extend(all_leds)
    shuffled_leds.extend(all_leds)
    random.shuffle(shuffled_leds)
    for led in shuffled_leds:
        led.toggle()
        sleep(0.2)
