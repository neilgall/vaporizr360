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

    def _output(self, pin, state):
        value = gpio.HIGH if state else gpio.LOW
        gpio.output(pin, value)

    def stop(self):
        "Stop the car moving"
        self._output(Car.LEFT_BACKWARD, 0)
        self._output(Car.RIGHT_BACKWARD, 0)
        self._output(Car.LEFT_FORWARD, 0)
        self._output(Car.RIGHT_FORWARD, 0)

    def forward(self):
        "Drive the car forwards"
        self._output(Car.LEFT_BACKWARD, 0)
        self._output(Car.RIGHT_BACKWARD, 0)
        self._output(Car.LEFT_FORWARD, 1)
        self._output(Car.RIGHT_FORWARD, 1)

    def backward(self):
        "Drive the car backwards"
        self._output(Car.LEFT_FORWARD, 0)
        self._output(Car.RIGHT_FORWARD, 0)
        self._output(Car.LEFT_BACKWARD, 1)
        self._output(Car.RIGHT_BACKWARD, 1)

    def spinLeft(self):
        "Spin the car on the spot to the left"
        self._output(Car.LEFT_FORWARD, 0)
        self._output(Car.RIGHT_BACKWARD, 0)
        self._output(Car.LEFT_BACKWARD, 1)
        self._output(Car.RIGHT_FORWARD, 1)

    def spinRight(self):
        "Spin the car on the spot to the right"
        self._output(Car.LEFT_BACKWARD, 0)
        self._output(Car.RIGHT_FORWARD, 0)
        self._output(Car.LEFT_FORWARD, 1)
        self._output(Car.RIGHT_BACKWARD, 1)

    def drive(self, left, right):
        if left > 0:
            self._output(Car.LEFT_BACKWARD, 0)
            self._output(Car.LEFT_FORWARD, 1)
        elif left < 0:
            self._output(Car.LEFT_FORWARD, 0)
            self._output(Car.LEFT_BACKWARD, 1)
        else:
            self._output(Car.LEFT_FORWARD, 0)
            self._output(Car.LEFT_BACKWARD, 0)

        if right > 0:
            self._output(Car.RIGHT_BACKWARD, 0)
            self._output(Car.RIGHT_FORWARD, 1)
        elif right < 0:
            self._output(Car.RIGHT_FORWARD, 0)
            self._output(Car.RIGHT_BACKWARD, 1)
        else:
            self._output(Car.RIGHT_BACKWARD, 0)
            self._output(Car.RIGHT_FORWARD, 0)
            
