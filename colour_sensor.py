# Write your code here :-)
import board
import busio
import adafruit_tcs34725
from time import sleep

print("Hewo wowwd")

i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
while not i2c.try_lock():
    pass

print("Scanning I2C bus...")
devices = i2c.scan()
print("I2C addresses found:", [hex(d) for d in devices])
i2c.unlock()

sensor = adafruit_tcs34725.TCS34725(i2c)

while True:
    print('Color: ({0}, {1}, {2})'.format(*sensor.color_rgb_bytes))
    print('Temperature: {0}K'.format(sensor.color_temperature))
    print('Lux: {0}'.format(sensor.lux))
    sleep(1)
