# paint

Python code to integrate with the hardware for paint.

Passes messages one way from a microprocessor (CircuitPlayground Bluefruit, or Pi Pico or whatever) down a USB cable and publishes them to MQTT.

## cp.py

Run on the microprocessor.

Prints stuff to stdout.

Honestly this is not the important bit, just write your Python script to print whatever you want to stdout.

## laptop.py

Run on the host. Connects to the COM port that the microprocessor is connected to, and publishes its stdout to MQTT on the `paint` topic.

It's intended for use entirely locally to the laptop (i.e. running a local mosquitto) but no reason you couldn't use it for something remote.

### Zero to Hero

Connect the microprocessor to your laptop over USB. Go to Windows Device Manager > Ports (COM & LPT) > you should see the device there and it'll say e.g. COM3. Update line 4 of laptop.py if it's on a different port.

> I'm seeing an Unauthorised error when trying to connect.

Make sure you've closed Mu or any other Python editors that might be using the port, and try again.


