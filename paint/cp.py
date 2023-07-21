from adafruit_circuitplayground import cp
import time
import board
import busio

a = 0
b = -1
colour = (10,10,10)

def select_tool(num):
    if num == 0:
        print("pencil")
    elif num == 1:
        print("fill")
    elif num == 2:
        print("erase")
    else:
        print("line")

def select_colour(num):
    if num == 0:
        print("red")
        return (30, 0, 0)
    if num == 1:
        print("yellow")
        return (20, 10, 0)
    if num == 2:
        print("green")
        return (0, 30, 0)
    else:
        print("blue")
        return (0, 0, 30)

while True:
    if cp.button_a:
        a = (a + 1) % 4
        select_tool(a)

    if cp.button_b:
        b = (b + 1) % 4
        colour = select_colour(b)

    cp.pixels.fill((0,0,0))
    cp.pixels[a] = colour
    time.sleep(0.2)

