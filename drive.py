import math
import time
import xbox
from vaporizr import Car

def drive(car, x, y):
    if abs(x) > abs(y):
        car.drive(0, x)
    elif y > 0:
        car.forward()
    elif y < 0:
        car.backward()
    else:
        car.stop()

    magnitude = math.sqrt(x * x + y * y)
    left_speed = magnitude * y * (1 + x)
    right_speed = magnitude * y * (1 - x)
    stepper.set_left_speed(left_speed)
    stepper.set_right_speed(right_speed)

if __name__ == "__main__":
    joy = xbox.Joystick()
    car = Car()

    try:
        while not joy.Start():
            if joy.dpadLeft():
                car.spinLeft()
            elif joy.dpadRight():
                car.spinRight():
            else:
                drive(car, joy.leftX(), joy.leftY())
    finally:
        car.stop()
        joy.close()
