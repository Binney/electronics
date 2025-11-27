from math import cos, sin, radians
import os

import time as system_time

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

# The display is 320x240 pixels
display = board.DISPLAY
display.rotation = 0 # Rotate the display set to 0 if you want it upright, 180 for lying flat

# Set up touchscreen
ctp = adafruit_cst8xx.Adafruit_CST8XX(board.I2C())
events = adafruit_cst8xx.EVENTS

# Get WiFi details, ensure these are setup in settings.toml
ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")
weather_url = "https://api.open-meteo.com/v1/forecast?latitude=51.5085&longitude=-0.1257&hourly=temperature_2m&timezone=auto&forecast_days=1"

# Initalize Wifi, Socket Pool, Request Session
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)
rssi = wifi.radio.ap_info.rssi

print(f"\nConnecting to {ssid}...")
print(f"Signal Strength: {rssi}")
try:
    # Connect to the Wi-Fi network
    wifi.radio.connect(ssid, password)
except OSError as e:
    print(f"❌ OSError: {e}")
print("✅ Wifi!")

ntp = adafruit_ntp.NTP(pool, tz_offset=0)  # tz_offset in hours (0 for UTC, or -5 for EST, etc.)

def arrow(size, skew, thickness, x, y, angle):
    points = [(0, 0), (size, skew), (size + thickness, skew), (thickness, 0), (size + thickness, -skew), (size, -skew)]
    points = [
        (int(round(px * cos(angle) - py * sin(angle))),
         int(round(px * sin(angle) + py * cos(angle))))
        for px, py in points
    ]
    points = [(p[0] + x, p[1] + y) for p in points]
    return FilledPolygon(points, fill=0xdb010e)

r1 = 95
r2 = 83

# Main loop
while True:
    now = system_time.monotonic()

    my_display_group = displayio.Group()

    inner_clock_outline = Circle(display.width // 2, display.height // 2, r1 + 2, outline=0xdb010e, stroke=5)
    outer_clock_outline = Circle(display.width // 2, display.height // 2, r2 + 3, outline=0xdb010e, stroke=5)
    my_display_group.append(inner_clock_outline)
    my_display_group.append(outer_clock_outline)

    rtc.RTC().datetime = ntp.datetime
    time_value = system_time.localtime()
    time_label = label.Label(terminalio.FONT, text=f"{time_value.tm_hour:02d}:{time_value.tm_min:02d}", color=0xFFFFFF, scale=3)
    time_label.anchor_point = (0.5, 0.5)
    time_label.anchored_position = (display.width // 2, display.height // 2)
    my_display_group.append(time_label)

    # seconds = time_value.tm_sec
    # we are actually faking this entirely
    seconds = (now % 60) + (now % 1)
    angle = radians(seconds * 6 + 180)
    sec_hand_coords = (display.width // 2 + int(r1 * -1 * sin(angle)),
                       display.height // 2 + int(r1 * cos(angle)))
    tr1 = arrow(15, 11, 7, sec_hand_coords[0], sec_hand_coords[1], angle)
    my_display_group.append(tr1)

    sec_hand_coords = (display.width // 2 + int(r2 * -1 * sin(angle)),
                       display.height // 2 + int(r2 * cos(angle)))
    tr2 = arrow(-15, 11, -7, display.width - sec_hand_coords[0], sec_hand_coords[1], -angle)
    my_display_group.append(tr2)

    # Here's an example of how to use the touch screen. Docs: https://docs.circuitpython.org/projects/cst8xx/en/latest/
    # The touchscreen is intialised at the start of the program
    # You only get the x, y coordinates of the touch, so you'll have to cross reference that with the coordinates you put your ui elements at.
    # touch_text = "no touch detected"
    # if ctp.touched:
    #     touch = ctp.touches[0]
    #     x = touch["x"]
    #     y = touch["y"]
    #     event = events[touch["event_id"]]
    #     touch_text = f"touch at x: {x}, y: {y}, event: {event}"

    # touch_label = label.Label(terminalio.FONT, text=touch_text)
    # touch_label.x = 20
    # touch_label.y = 200
    # my_display_group.append(touch_label)

    display.root_group = my_display_group

    

