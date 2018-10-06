from enum import Enum
import queue
import threading
import time

TICKS_PER_SECOND = 10

class Commands(Enum):
    KILL = 1
    SET_LEFT_SPEED = 2
    SET_RIGHT_SPEED = 3

class Stepper:
    def __init__(self, car):
        self._car = car
        self._queue = queue.Queue()
        self._tick = 0
        self._left_speed = 0
        self._right_speed = 0
        self._thread = threading.Thread(target=self._bg_main)
        self._thread.start() 

    def stop(self):
        "Stop the stepper"
        self._queue.put((Commands.KILL, None))
        self._thread.join()

    def set_left_speed(self, speed):
        "Set left wheel speed in range [-1..1]"
        self._queue.put((Commands.SET_LEFT_SPEED, speed))

    def set_right_speed(self, speed):
        "Set right wheel speed in range [-1..1]"
        self._queue.put((Commands.SET_RIGHT_SPEED, speed))

    def _bg_main(self):
        while True:
            self._step()
            if not self._queue.empty():
                cmd, arg = self._queue.get()
                if self._dispatch(cmd, arg):
                    break
            time.sleep(1.0/TICKS_PER_SECOND)
        self._car.stop()

    def _dispatch(self, cmd, arg):
        if cmd == Commands.KILL:
            return True
        elif cmd == Commands.SET_LEFT_SPEED:
            self._left_speed = int(arg * TICKS_PER_SECOND)
        elif cmd == Commands.SET_RIGHT_SPEED:
            self._right_speed = int(arg * TICKS_PER_SECOND)
    
    def _step(self):   
        left = self._direction_for_speed(self._left_speed)
        right = self._direction_for_speed(self._right_speed) 
        self._car.drive(left, right)
        self._tick = (self._tick + 1) % TICKS_PER_SECOND

    def _direction_for_speed(self, speed):
        enable = 1 if self._tick < abs(speed) else 0
        return -enable if speed < 0 else enable

