import RPi.GPIO as gpio

class Lamp:
    def __init__(self, pin):
        self._pin = pin
        self._state = gpio.LOW
        gpio.setmode(gpio.BCM)
        gpio.setup(self._pin, gpio.OUT)

    def _update(self):
        gpio.output(self._pin, self._state)

    def toggle(self):
        if self._state == gpio.LOW:
            self._state = gpio.HIGH
        else:
            self._state = gpio.LOW
        self._update()

    def off(self):
        self._state = gpio.LOW
        self._update()

    def on(self):
        self._state = gpio.HIGH
        self._update()
