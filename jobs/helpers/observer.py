import math

from utils.config import Config
from processes.move import Move
from processes.wait import Wait
from shapes.window import Window
from shapes.rect import Rect
from jobs.helpers.navigator import get_npc

OBSERVE_Y = 0
OBSERVE_Y_INV = 1
OBSERVE_X = 2
OBSERVE_X_INV = 3
DELTA = 3
OBSERVE_DELAY = 0.05

# start point camera position reqiuirement
CAMERA_HEIGHT_LOWER = 300
CAMERA_HEIGHT_UPPER = 310
ANGLE_WIDTH = 10

config = Config()

def observe_height():
    titleRoi = get_npc(config.CharTitleConfig)
    height = camera_height(titleRoi)
    observable = config.Observable
    ch_lower, ch_upper = observable.camera_height_lower, observable.camera_height_upper
    if height > ch_lower and height <= ch_upper:
        return None
    return ch_lower - height

def observe_angle():
    titleRoi = get_npc(config.CharTitleConfig)
    width = camera_angle_width(titleRoi)
    # import cv2
    # import numpy as np
    # from utils.cv2_utils import show_image, screenshot
    # img = screenshot(Window().rect)
    # img = np.array(img)
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # cv2.circle(img, Window().relative_center(), 10, 255, 2)
    # show_image(img)
    if width >= 0 and width < ANGLE_WIDTH:
        return None
    return width

def camera_height(npc):
    npcC = _center(npc)
    return Window().relative_center()[1] - 10 - npcC[1]

def camera_angle_width(npc):
    npcC = _center(npc)
    screenC = Window().relative_center()
    return npcC[0] - screenC[0] + 15 # calibrate coef

def _center(rect1):
    return Rect(rect1).center()

class Observer:

    def __init__(self, xChecker, yChecker):
        self.move = Move()
        self.xChecker = xChecker
        self.yChecker = yChecker
        self.window = Window().center()

    def observe(self):
        xCheck = self.xChecker()
        yCheck = self.yChecker()
        if yCheck:
            self.direction = OBSERVE_Y
            self.round(yCheck, self.yChecker)
        if xCheck:
            self.direction = OBSERVE_X if xCheck > 0 else OBSERVE_X_INV
            self.round(xCheck, self.xChecker, axis='X')

    def round(self, initial, checker, axis='Y'):
        x, y = self.window
        dx, dy = x, y
        self.move.moveTo(x,y)
        self.move.pressRight()
        self._cast_direction(initial, axis)
        check = abs(initial)

        while check is not None:
            speed = math.floor(int(check / 10))
            if speed == 0:
                speed = 1

            for i in range(speed):
                self.move.move(self._apply_direction())
                Wait(OBSERVE_DELAY).delay()
            
            check = checker()
            self._cast_direction(check, axis)
            check = abs(check) if check is not None else None
        self.move.releaseRight()

    def _cast_direction(self, value, axis):
        if value is None:
            return
        if axis is 'Y':
            self.direction = OBSERVE_Y_INV if value < 0 else OBSERVE_Y
        if axis is 'X':
            self.direction = OBSERVE_X_INV if value < 0 else OBSERVE_X

    def _apply_direction(self):
        if self.direction is OBSERVE_Y:
            return 'Y'
        elif self.direction is OBSERVE_Y_INV:
            return 'U'
        elif self.direction is OBSERVE_X:
            return 'X'
        elif self.direction is OBSERVE_X_INV:
            return 'Z'
        else: None