from gpiozero import Button, LED
import time
import random

print("letsgo")

letter_0i = LED(2)
letter_1t = LED(3)
letter_2s = LED(4)
letter_3n = LED(17)
letter_4o = LED(27)
letter_5t = LED(22)
letter_6a = LED(10)
letter_7b = LED(9)
letter_8u = LED(11)
letter_9g = LED(5)

letter_10i = LED(15)
letter_11t = LED(18)
letter_12s = LED(23)
letter_13a = LED(24)
letter_14f = LED(25)
letter_15e = LED(8)
letter_16a = LED(7)
letter_17t = LED(12)
letter_18u = LED(16)
letter_19r = LED(20)
letter_20e = LED(21)

actual_sequence = [
    letter_12s,
    letter_18u,
    letter_7b,
    letter_1t,
    letter_15e,
    letter_19r,
    letter_19r,
    letter_6a
    ]

while True:
    for i in len(actual_sequence):
        actual_sequence[i].on()
        time.sleep(1)
        actual_sequence[i].off()
        time.sleep(0.5)
    time.sleep(3)

