import pyautogui as ui
from utils.serial_controller import SerialController
from processes.wait import Wait

X_DIRECT = ('X', 'Z')
Y_DIRECT = ('Y', 'U')
ACCURACY = 3

class Move:

    def __init__(self):

        self.serial = SerialController().serial
    
    def fromTo(self, start, end):
        self.start = start
        self.end = end
        startX, startY = self.start
        self.moveTo(startX, startY)
        self.pressRight()
        endX, endY = self.end
        self.moveTo(endX, endY)
        self.releaseRight()

    def moveTo(self, x, y):
        _x, _y = ui.position()
        axis = 'X'
        is_x_pass = self._get_axis_pass(x, _x)
        is_y_pass = self._get_axis_pass(y, _y)
        while not (is_x_pass and is_y_pass):
            if axis == 'X':
                if self._is_coord_less(_x, x):
                    self.move(X_DIRECT[1])
                    axis = 'Y' if not is_y_pass else 'X'
                else:
                    self.move(X_DIRECT[0])
                    axis = 'Y' if not is_y_pass else 'X'
            if axis == 'Y':
                if self._is_coord_less(_y, y):
                    self.move(Y_DIRECT[1])
                    axis = 'X' if not is_x_pass else 'Y'
                else:
                    self.move(Y_DIRECT[0])
                    axis = 'X' if not is_x_pass else 'Y'
            _x, _y = ui.position()
            is_x_pass = self._get_axis_pass(x, _x)
            is_y_pass = self._get_axis_pass(y, _y)

    def pressRight(self):
        self.serial.write(b'P')

    def releaseRight(self):
        self.serial.write(b'R')

    def _get_axis_pass(self, target_point, actual_point):
        return self._is_coord_less(actual_point, target_point) and self._is_coord_greater(actual_point, target_point)

    @staticmethod
    def _is_coord_less(current, target):
        return current >= target - ACCURACY

    @staticmethod
    def _is_coord_greater(current, target):
        return current <= target + ACCURACY

    def move(self, t):
        if t is None:
            return
        self.serial.write(t.encode())
