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

first_row = [
    letter_0i,
    letter_1t,
    letter_2s,
    letter_3n,
    letter_4o,
    letter_5t,
    letter_6a,
    letter_7b,
    letter_8u,
    letter_9g
    ]

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

second_row = [
    letter_10i,
    letter_11t,
    letter_12s,
    letter_13a,
    letter_14f,
    letter_15e,
    letter_16a,
    letter_17t,
    letter_18u,
    letter_19r,
    letter_20e
    ]

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

# Startup sequence
for i in range(0, 20):
    if i >= 10:
        first_row[i % 10].on()
    else:
        second_row[i % 10].on()
    time.sleep(1 / (i + 1))
for i in range(0, 10):
    first_row[i].on()
    second_row[i].on()
    time.sleep(0.1)
second_row[10].on()
for i in range(0, 10):
    first_row[i].off()
    second_row[i].off()
    time.sleep(0.1)
second_row[10].off()

print("Starting sequence")

while True:
    for led in actual_sequence:
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(0.5)
    print("Restart")
    time.sleep(3)

