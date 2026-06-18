'''
Wiring:
- GP0 to MOSFETTI A in
- GP2 to MOSFETTI B in
- GP4 to MOSFETTI C in
- GND to MOSFETTI GND in
- +5v, 12v, 24v as needed to Mosfetti power
- Strip power to Mosfetti A out +
- Strip R to Mofetti A out -
- Strip G to Mofetti B out -
- Strip B to Mofetti C out -
'''

import time
import board
import pwmio

r_led = pwmio.PWMOut(board.GP0, frequency=5000, duty_cycle=0)
g_led = pwmio.PWMOut(board.GP2, frequency=5000, duty_cycle=0)
b_led = pwmio.PWMOut(board.GP4, frequency=5000, duty_cycle=0)

def rainbow(theta):
    """Convert a hue to RGB values."""
    theta = theta % 360
    if theta < 60:
        r = 1.0
        g = theta / 60.0
        b = 0.0
    elif theta < 120:
        r = (120 - theta) / 60.0
        g = 1.0
        b = 0.0
    elif theta < 180:
        r = 0.0
        g = 1.0
        b = (theta - 120) / 60.0
    elif theta < 240:
        r = 0.0
        g = (240 - theta) / 60.0
        b = 1.0
    elif theta < 300:
        r = (theta - 240) / 60.0
        g = 0.0
        b = 1.0
    else:
        r = 1.0
        g = 0.0
        b = (360 - theta) / 60.0

    return int(r * 65535), int(g * 65535), int(b * 65535)

while True:
    for i in range(360):
        r, g, b = rainbow(i)
        r_led.duty_cycle = r
        g_led.duty_cycle = g
        b_led.duty_cycle = b
        time.sleep(0.01)
