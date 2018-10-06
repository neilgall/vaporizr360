import RPi.GPIO as gpio

class Car:
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
