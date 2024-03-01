import board
import rotaryio

encoderL = rotaryio.IncrementalEncoder(board.GP3, board.GP4)
last_position_L = None
encoderR = rotaryio.IncrementalEncoder(board.GP14, board.GP15)
last_position_R = None

print("start!")

while True:
    position = encoderL.position
    if last_position_L != position:
        print("L: " + str(position))
    last_position_L = position

    position = encoderR.position
    if last_position_R != position:
        print("R: " + str(position))
    last_position_R = position
