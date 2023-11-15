import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

print("asdlfkjasdflkasdflk")

GPIO_TRIGGER = 23
GPIO_ECHO = 24

booze_pin = 14

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(booze_pin, GPIO.IN)

GPIO.output(GPIO_TRIGGER, False)
time.sleep(2)
print("asdflkjeiqwqq111")

max_time = 1

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()
    ActualStartTime = time.time()
    print("initialSt: %1f." % StartTime)
    print("initialSp: %1f." % StopTime)
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
        if StartTime - ActualStartTime > max_time:
            print("something weird happened")
            return 0

    print("StartTime: %1f." % StartTime)

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
        if StopTime - StartTime > max_time:
            print("something else weird happened")
            return 0
    print("StopTime:  %1f." % StopTime)

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

time_to_smell = 1000

def test_approval():
    n = 0
    alcohol_absent_count = 0
    while n < time_to_smell:
        alcohol_absent_count += GPIO.input(booze_pin)
        time.sleep(0.01)
        n += 1
    print("Verdict:")
    print(alcohol_absent_count)
    if alcohol_absent_count < 1000:
        print("boooooze")
        return True
    else:
        print("no booz")
        return False

while True:
    print("wat is distance")
    dist = distance()
    print("Distance is: %.1f" % dist)
    if dist < 15:
        print("cocktail detected!!!")
        print("but does Dom approve?")
        does_dom_approve = test_approval()
        if does_dom_approve:
            print("Dom approves!")
        else:
            print("Dom does not approve :(")
    time.sleep(1)

