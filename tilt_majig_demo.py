print("Hello world!")

from adafruit_circuitplayground import cp
import time
import rainbowio
import math

def angle_in_degrees(x, y):
    """Return the angle of the point (x, y), in degrees from -180 to 180"""
    return math.atan2(y, x) / math.pi * 180


def positive_degrees(angle):
    """Convert -180 through 180 to 0 through 360"""
    return (angle + 360) % 360

def get_tilt():
    """Normalize the Y-Axis Tilt
    standard_gravity = (
        9.81  # Acceleration (m/s²) due to gravity at the earth’s surface
    )
    print(cp.acceleration)
    constrained_accel = min(max(0.0, -cp.acceleration[1]), standard_gravity)
    return constrained_accel / standard_gravity
    """
    accel_x, accel_y = cp.acceleration[:2]  # Ignore z
    return positive_degrees(angle_in_degrees(accel_x, accel_y)) / 360

def times(number, input_tuple):
    return tuple(map(lambda x: x * number, input_tuple))

def hsv_to_rgb(hue, brightness):
    hue = hue % 1
    if hue < 0.3333333:
        return times(brightness, (0.333333 - hue, hue, 0))
    if hue < 0.6666666:
        return times(brightness, (0, 0.666666 - hue, hue - 0.3333333))
    else:
        return times(brightness, (hue - 0.6666666, 0, 1 - hue))

def freq_for(number):
    STARTING_NOTE = 233.08
    return STARTING_NOTE * 2 ** (number)

counter = 0

while True:
    #counter += 0.01
    #cp.pixels.fill((5, 1, 0))
    tilt = get_tilt()
    cp.pixels.fill(hsv_to_rgb(tilt, 100))
    cp.stop_tone()
    #cp.start_tone(freq_for(tilt))
    time.sleep(0.1)
