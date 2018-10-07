import math
import time
import xbox
from lamp import Lamp
from vaporizr import Car

def init_controller():
    lamp = Lamp(pin=25)
    while True:
        try:
            joy = xbox.Joystick()
            lamp.on()
            return joy
        except Exception as e:
            print(e)
            lamp.on()
            time.sleep(0.5)
            lamp.off()
            time.sleep(0.5)

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
