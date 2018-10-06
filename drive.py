import math
import time
import xbox
from vaporizr import Car

def init_controller():
    while True:
        try:
            return xbox.Joystick()
        except Exception as e:
            print(e)
            time.sleep(5)

def drive(car, x, y):
    if abs(x) > abs(y):
        car.drive(1, 0) if x > 0 else car.drive(0, 1)
    elif y > 0:
        car.forward()
    elif y < 0:
        car.backward()
    else:
        car.stop()

if __name__ == "__main__":
    joy = init_controller()
    car = Car()

    try:
        while not joy.Start():
            if joy.dpadLeft():
                car.spinLeft()
            elif joy.dpadRight():
                car.spinRight()
            else:
                drive(car, joy.leftX(), joy.leftY())
    finally:
        car.stop()
        joy.close()
