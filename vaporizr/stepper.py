from enum import Enum
import time

class Commands(Enum):
    KILL = 1
    SET_LEFT_SPEED = 2
    SET_RIGHT_SPEED = 3

class Stepper:
    def __init__(self, car):
        self._car = car
        self._tick = 0
        self._ticks_per_second = 20
        self._left_speed = 0
        self._right_speed = 0
        self._start_time = time.time()

    def set_left_speed(self, speed):
        "Set left wheel speed in range [-1..1]"
        self._left_speed = speed * self._ticks_per_second

    def set_right_speed(self, speed):
        "Set right wheel speed in range [-1..1]"
        self._right_speed = speed * self._ticks_per_second

    def step(self):   
        tick = ((time.time() - self._start_time) * self._ticks_per_second) % self._ticks_per_second
        left = self._direction_for_speed(tick, self._left_speed)
        right = self._direction_for_speed(tick, self._right_speed) 
        self._car.drive(left, right)

    def _direction_for_speed(self, tick, speed):
        enable = 1 if tick < abs(speed) else 0
        return -enable if speed < 0 else enable

