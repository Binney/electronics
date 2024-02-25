from RpiMotorLib import RpiMotorLib

print("Hello, world!")

GpioPins = [14, 15, 18, 23]
mymotortest = RpiMotorLib.BYJMotor("SyzyMotor", "28BYJ")
mymotortest.motor_run(GpioPins, 0.001, 512, False, False, "half", 0.05)

print("And that's done")
