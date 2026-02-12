from math import cos, sin, radians
import os

import time as system_time
from time import sleep

import adafruit_connection_manager
import wifi

import adafruit_requests

import board
import terminalio
import displayio
from adafruit_display_text import label
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.filled_polygon import FilledPolygon

import adafruit_ntp
import rtc

import adafruit_cst8xx
from adafruit_bitmap_font import bitmap_font

# The display is 320x240 pixels
display = board.DISPLAY
display.rotation = 0 # Rotate the display set to 0 if you want it upright, 180 for lying flat

# Set up touchscreen
ctp = adafruit_cst8xx.Adafruit_CST8XX(board.I2C())
events = adafruit_cst8xx.EVENTS

connected = False
wifi_try = 0

# Get WiFi details, ensure these are setup in settings.toml
ssids = os.getenv("KNOWN_WIFIS")
passwords = os.getenv("KNOWN_WIFI_PASSWORDS")

while not connected:
    ssid = ssids.split(",")[wifi_try].strip()
    password = passwords.split(",")[wifi_try].strip()

    try:
        print(f"\nConnecting to {ssid}...")
        wifi.radio.connect(ssid, password)
        connected = True
    except Exception as e:
        print(f"❌ Error: {e}")
        wifi_try += 1
        if wifi_try >= len(ssids.split(",")):
            wifi_try = 0
            sleep(5)
print("✅ Wifi!")

# Initalize Wifi, Socket Pool, Request Session
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)

found_ntp = False
while not found_ntp:
    try:
        ntp = adafruit_ntp.NTP(pool, tz_offset=0)  # tz_offset in hours (0 for UTC, or -5 for EST, etc.)
        found_ntp = True
    except Exception as e:
        print(f"❌ NTP Error: {e}")
print("✅ NTP!")

font = bitmap_font.load_font("fonts/logisoso46.bdf")

def arrow(size, skew, thickness, x, y, angle):
    points = [(0, 0), (size, skew), (size + thickness, skew), (thickness, 0), (size + thickness, -skew), (size, -skew)]
    points = [(p[0] - size * 1.5 // 2, p[1]) for p in points]
    points = [
        (int(round(px * cos(angle) - py * sin(angle))),
         int(round(px * sin(angle) + py * cos(angle))))
        for px, py in points
    ]
    points = [(p[0] + x, p[1] + y) for p in points]
    return FilledPolygon(points, fill=0xdb010e)

r1 = 95
r2 = 83

start_time = (system_time.monotonic() - system_time.localtime().tm_sec) // 1
last_frame_time = system_time.monotonic()
seconds = system_time.localtime().tm_sec
frames = 0

while True:
    frames += 1
    my_display_group = displayio.Group()

    inner_clock_outline = Circle(display.width // 2, display.height // 2, r1 + 2, outline=0xdb010e, stroke=5)
    outer_clock_outline = Circle(display.width // 2, display.height // 2, r2 + 3, outline=0xdb010e, stroke=5)
    my_display_group.append(inner_clock_outline)
    my_display_group.append(outer_clock_outline)

    try:
        rtc.RTC().datetime = ntp.datetime
    except Exception as e:
        print(f"❌ RTC Error: {e}")
        pass  # if NTP fails, just keep going with last known time

    time_value = system_time.localtime()
    time_label = label.Label(font, text=f"{time_value.tm_hour:02d}:{time_value.tm_min:02d}", color=0xFFFFFF, scale=1)
    time_label.anchor_point = (0.5, 0.5)
    time_label.anchored_position = (display.width // 2, display.height // 2)
    my_display_group.append(time_label)

    # we tick every second and re-sync every minute,
    # so frames happen evenly
    seconds += 1
    if (seconds % 60) + 15 >= 60:
        # Loop back at the 15 sec mark, because the top and bottom are when the hands line up and that's pretty
        seconds = time_value.tm_sec
    angle = radians(seconds * 6 + 180)
    sec_hand_coords = (display.width // 2 + int((r1 + 1) * -1 * sin(angle)),
                       display.height // 2 + int((r1 + 1) * cos(angle)))
    tr1 = arrow(25, 11, 10, sec_hand_coords[0], sec_hand_coords[1], angle)
    my_display_group.append(tr1)

    sec_hand_coords = (display.width // 2 + int((r2 + 1) * -1 * sin(angle)),
                       display.height // 2 + int((r2 + 1) * cos(angle)))
    tr2 = arrow(-25, 11, -10, display.width - sec_hand_coords[0], sec_hand_coords[1], -angle)
    my_display_group.append(tr2)

    display.root_group = my_display_group

    # force frames to happen once a second regardless of real time
    delta = system_time.monotonic() - last_frame_time
    if delta < 1:
        sleep(1 - delta)
    else:
        # would be nice to do another alignment but fine for now, it'll sync within 1min
        pass
    last_frame_time = system_time.monotonic()

