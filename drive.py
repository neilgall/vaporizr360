import RPi.GPIO as gpio
import xbox
import time
import math

class Car(object):
    "R/C controller"
    RIGHT_FORWARD = 22
    RIGHT_BACKWARD = 27
    LEFT_FORWARD = 24
    LEFT_BACKWARD = 23
    PINS = [RIGHT_FORWARD, RIGHT_BACKWARD, LEFT_FORWARD, LEFT_BACKWARD]

    def __init__(self):
        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)
        for pin in Car.PINS:
            gpio.setup(pin, gpio.OUT)
            gpio.output(pin, gpio.LOW)

    def close(self):
        "Shut down the driver"
        self.stop()
        gpio.cleanup()

    def _output(self, pins, state):
        value = gpio.HIGH if state else gpio.LOW
        for pin in pins:
            gpio.output(pin, value)

    def stop(self):
        "Stop the car moving"
        self._output(Car.PINS, 0)

    def forward(self):
        "Drive the car forwards"
        self.stop()
        self._output([Car.LEFT_FORWARD, Car.RIGHT_FORWARD], 1)

    def backward(self):
        "Drive the car backwards"
        self.stop()
        self._output([Car.LEFT_BACKWARD, Car.RIGHT_BACKWARD], 1)

    def spinLeft(self):
        "Spin the car on the spot to the left"
        self.stop()
        self._output([Car.LEFT_BACKWARD, Car.RIGHT_FORWARD], 1)

    def spinRight(self):
        "Spin the car on the spot to the right"
        self.stop()
        self._output([Car.LEFT_FORWARD, Car.RIGHT_BACKWARD], 1)

    def drive(self, left, right):
        self.stop()
        pins = []
        if left > 0: pins.append(Car.LEFT_FORWARD)
        elif left < 0: pins.append(Car.LEFT_BACKWARD)
        if right > 0: pins.append(Car.RIGHT_FORWARD)
        elif right < 0: pins.append(Car.RIGHT_BACKWARD)
        self._output(pins, 1)

class AnalogMapper(object):
    "Map analog stick values to discrete car controls"
    def __init__(self, car, ticks = 100):
        self.car = car
        self.leftSpeed = 0
        self.rightSpeed = 0
        self.tickCount = 0
        self.ticksPerSecond = ticks

    def setStick(self, x, y):
        "Set the stick X and Y coordinates in the range [-1..+1]"
        magnitude = math.sqrt(x * x + y * y)
        self.leftSpeed = magnitude * y * (1 + x)
        self.rightSpeed = magnitude * y * (1 - x)

    def tick(self):
        "Advance the tick counter and update the car drive state"
        if self.tickCount == 0:
            self.tickCount = self.ticksPerSecond
        else:
            self.tickCount -= 1

        left = self.enabled(self.leftSpeed)
        right = self.enabled(self.rightSpeed)
        print(self.leftSpeed, self.rightSpeed, self.tickCount, left, right)

        self.car.drive(left, right)

    def enabled(self, speed):
        decisecond = self.tickCount % 10
        enableDeciseconds = int(abs(speed) * self.ticksPerSecond / 10)
        if enableDeciseconds > decisecond:
            return speed
        else:
            return 0

if __name__ == "__main__":
    joy = xbox.Joystick()
    car  = Car()
    mapper = AnalogMapper(car)

    while not joy.Guide():
        mapper.setStick(joy.leftX(), joy.leftY())
        mapper.tick()
        time.sleep(0.01)

    car.close()
    joy.close()
