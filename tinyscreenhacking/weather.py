import os

import time as system_time

import adafruit_connection_manager
import wifi

import adafruit_requests

import board
import terminalio
import displayio
from adafruit_display_text import label
from adafruit_display_shapes.roundrect import RoundRect

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

print(f" | ✅ JSON GET Test: {weather_url}")
with requests.get(weather_url) as response:
    json_resp = response.json()
    print(json_resp)
    # Parse out the 'data' key from json_resp dict.
    print(f" | ✅ JSON 'value' Response: {json_resp['timezone']}")
print("-" * 80)

# Set text, font, and color
font = terminalio.FONT
color = 0x0000FF

time_temp = []
for i in range(len(json_resp["hourly"]["time"])):
    time = json_resp["hourly"]["time"][i]
    temp = json_resp["hourly"]["temperature_2m"][i]
    time_temp.append([time, temp])
    

UPDATE_INTERVAL_MS = int(os.getenv("UPDATE_INTERVAL_MS"))
start_time = system_time.monotonic()

current_index = 0 # keeps track of the index of the temperature we're showing

# Main loop
while True:
    current_time = system_time.monotonic()
    
    # The body of this if statement is only run every UPDATE_INTERVAL_MS milliseconds
    if current_time - start_time > (UPDATE_INTERVAL_MS/1000.0):
        # Maybe you could call an api here?
        current_index += 1
        current_index = current_index % len(time_temp)
        start_time = current_time


    # The code below uses the drawing api to render to the screen, see https://learn.adafruit.com/circuitpython-display-support-using-displayio/ui-quickstart
    my_display_group = displayio.Group() # https://learn.adafruit.com/circuitpython-display-support-using-displayio/ui-quickstart#groups-3033357
    header_card = RoundRect(10, 10, 300, 40, 10, fill=0x0, outline=0xFF00FF, stroke=3)
    my_display_group.append(header_card) # Display group to contain the elements

    heading = label.Label(terminalio.FONT, text="Temperature in London", color=0xFFFFFF)
    heading.x = 30
    heading.y = 30
    heading.scale = 2
    my_display_group.append(heading)

    debug_text = label.Label(terminalio.FONT, text=f"got {len(time_temp)} temps from api, showing {current_index}\n waiting {UPDATE_INTERVAL_MS}ms between updates,current-start=: {current_time-start_time}")
    debug_text.y = 60
    my_display_group.append(debug_text)
    

    time, temperature = time_temp[current_index]

    time_label = label.Label(terminalio.FONT, text=str(time))
    time_label.x = 50
    time_label.y = 100
    time_label.scale = 2
    my_display_group.append(time_label)

    temperature_label = label.Label(terminalio.FONT, text=str(temperature) + "C")
    temperature_label.x = 50
    temperature_label.y = 130
    temperature_label.scale = 3
    my_display_group.append(temperature_label)


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

    

