import RPi.GPIO as GPIO
import time

TRIG = 24
ECHO = 23



def measure(trig_pin, echo_pin):
    GPIO.setmode(GPIO.BCM)
    print("Distance measurement in progress")

    GPIO.setup(trig_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)

    GPIO.output(trig_pin, False)
    print("Waiting for sensor to settle")
    time.sleep(2)

    GPIO.output(trig_pin, True)
    time.sleep(0.00001)
    GPIO.output(trig_pin, False)

    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()

    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = round(pulse_duration * 17150, 2)
    print("Distance: " + str(distance))

    GPIO.cleanup()

while True:
    measure(24, 23)
