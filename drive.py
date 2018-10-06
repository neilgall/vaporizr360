import math
import time
import xbox
from vaporizr import Stepper, Car

def set_stepper(stepper, x, y):
    "Set the stick X and Y coordinates in the range [-1..+1]"
    magnitude = math.sqrt(x * x + y * y)
    left_speed = magnitude * y * (1 + x)
    right_speed = magnitude * y * (1 - x)
    stepper.set_left_speed(left_speed)
    stepper.set_right_speed(right_speed)

if __name__ == "__main__":
    joy = xbox.Joystick()
    stepper = Stepper(Car())

    try:
        while not joy.Start():
            set_stepper(stepper, joy.leftX(), joy.leftY())
            time.sleep(0.1)
    finally:
        stepper.stop()
        joy.close()
