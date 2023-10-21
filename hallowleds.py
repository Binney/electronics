from gpiozero import LED
from time import sleep
import random

G = LED(0)
H = LED(1)
O = LED(2)
S = LED(3)
T = LED(4)
I = LED(5)
D = LED(6)
C = LED(7)
L = LED(8)
U = LED(9)
E = LED(10)

answer = [G, O, O, U, T, S, I, D, E, D, I, G]

while True:
    for led in answer:
        led.on()
        sleep(2)
        led.off()
        sleep(1)

    # all blink complete sequence
    for i in range(5):
        for led in answer:
            led.on()
        sleep(1 / (i ** 2))
        for led in answer:
            led.off()

    sleep(5)

    shuffled_answer = answer.copy()
    shuffled_answer.append(answer)
    random.shuffle(shuffled_answer)
