from gpiozero import Button, LED
from time import sleep

wait = 0.001

ctrA = LED(14) # purple
ctrB = LED(15) # green
ctrC = LED(18) # orange
ctrD = LED(23) # white

while True:

    ctrA.on()
    ctrB.off()
    ctrC.off()
    ctrD.off()
    sleep(wait)

    ctrA.on()
    ctrB.on()
    ctrC.off()
    ctrD.off()
    sleep(wait)

    ctrA.off()
    ctrB.on()
    ctrC.off()
    ctrD.off()
    sleep(wait)

    ctrA.off()
    ctrB.on()
    ctrC.on()
    ctrD.off()
    sleep(wait)

    ctrA.off()
    ctrB.off()
    ctrC.on()
    ctrD.off()
    sleep(wait)

    ctrA.off()
    ctrB.off()
    ctrC.on()
    ctrD.on()
    sleep(wait)

    ctrA.off()
    ctrB.off()
    ctrC.off()
    ctrD.on()
    sleep(wait)

    ctrA.on()
    ctrB.off()
    ctrC.off()
    ctrD.on()
    sleep(wait)


