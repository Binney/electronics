from tm1650 import TM1650
from time import sleep

SDA_PIN = 0
SCL_PIN = 1
disp = TM1650(SDA_PIN, SCL_PIN)

disp.display_on()
disp.display_clear()

disp.display_letter(0, 'A')
disp.display_letter(1, 'B')
disp.display_letter(2, 'C')
disp.display_letter(3, 'D')
sleep(1)

for i in range(10000):
  disp.display_integer(i)

disp.display_clear()
disp.off()
