# Write your code here :-)
print("Hello world!")

from adafruit_circuitplayground import cp
import time
import board
import busio

counter = 3
colour = 0

while True:
    if cp.button_a:
        counter += 1
        print(counter)

    if cp.button_b:
        colour = (colour + 1) % 30
        print("Colour: " + str(colour))
    cp.pixels.fill((0,0,0))
    cp.pixels[counter % 10] = (30 - colour, colour, 0)
    time.sleep(0.1)

