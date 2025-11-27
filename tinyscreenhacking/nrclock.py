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

# print(f" | ✅ JSON GET Test: {weather_url}")
# with requests.get(weather_url) as response:
#     json_resp = response.json()
#     print(json_resp)
#     # Parse out the 'data' key from json_resp dict.
#     print(f" | ✅ JSON 'value' Response: {json_resp['timezone']}")
# print("-" * 80)

# # Set text, font, and color
# font = terminalio.FONT
# color = 0x0000FF

# time_temp = []
# for i in range(len(json_resp["hourly"]["time"])):
#     time = json_resp["hourly"]["time"][i]
#     temp = json_resp["hourly"]["temperature_2m"][i]
#     time_temp.append([time, temp])
    

UPDATE_INTERVAL_MS = int(os.getenv("UPDATE_INTERVAL_MS"))
start_time = system_time.monotonic()

current_index = 0 # keeps track of the index of the temperature we're showing

def arrow(size, skew, thickness, x, y, angle):
    points = [(0, 0), (size, skew), (size + thickness, skew), (thickness, 0), (size + thickness, -skew), (size, -skew)]
    points = [(p[0] + x, p[1] + y) for p in points]
    return FilledPolygon(points, fill=0xFFFF00)

r1 = 80
r2 = 90

# Main loop
while True:
    # The code below uses the drawing api to render to the screen, see https://learn.adafruit.com/circuitpython-display-support-using-displayio/ui-quickstart
    my_display_group = displayio.Group() # https://learn.adafruit.com/circuitpython-display-support-using-displayio/ui-quickstart#groups-3033357

    inner_clock_outline = Circle(display.width // 2, display.height // 2, r1, outline=0xAA0000, stroke=4)
    outer_clock_outline = Circle(display.width // 2, display.height // 2, r2, outline=0xAA0000, stroke=4)
    my_display_group.append(inner_clock_outline)
    my_display_group.append(outer_clock_outline)

    rtc.RTC().datetime = ntp.datetime
    time_value = system_time.localtime()
    time_label = label.Label(terminalio.FONT, text=f"{time_value.tm_hour:02d}:{time_value.tm_min:02d}", color=0xFFFFFF, scale=3)
    time_label.anchor_point = (0.5, 0.5)
    time_label.anchored_position = (display.width // 2, display.height // 2)
    my_display_group.append(time_label)

    seconds = time_value.tm_sec
    sec_hand_coords = (display.width // 2 + int(r1 * -1 * sin(radians(seconds * 6))),
                       display.height // 2 + int(r1 * cos(radians(seconds * 6))))
    tr1 = arrow(10, 8, 8, sec_hand_coords[0], sec_hand_coords[1], 0)
    my_display_group.append(tr1)

    sec_hand_coords = (display.width // 2 + int(r2 * -1 * sin(radians(seconds * 6))),
                       display.height // 2 + int(r2 * cos(radians(seconds * 6))))
    tr2 = arrow(10, 8, 8, display.width - sec_hand_coords[0], sec_hand_coords[1], 0)
    my_display_group.append(tr2)

    # Here's an example of how to use the touch screen. Docs: https://docs.circuitpython.org/projects/cst8xx/en/latest/
    # The touchscreen is intialised at the start of the program
    # You only get the x, y coordinates of the touch, so you'll have to cross reference that with the coordinates you put your ui elements at.
    touch_text = "no touch detected"
    if ctp.touched:
        touch = ctp.touches[0]
        x = touch["x"]
        y = touch["y"]
        event = events[touch["event_id"]]
        touch_text = f"touch at x: {x}, y: {y}, event: {event}"

    touch_label = label.Label(terminalio.FONT, text=touch_text)
    touch_label.x = 20
    touch_label.y = 200
    my_display_group.append(touch_label)

    # Show the group we've just built up.
    display.root_group = my_display_group

    

