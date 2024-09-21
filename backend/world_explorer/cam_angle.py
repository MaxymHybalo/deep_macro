import cv2
import numpy as np
import sys,os
import time

sys.path.insert(0, os.getcwd())

from screen_reader import get_window_image
from driver import click, double, slide
from angle import camera_angle
from world_explorer.utils import window_center

handle = 1051262
x, y = window_center(handle)
ACC = 2 # how accurate angle
SLIDE_DELTA = 4
def in_bounds(value, bounding): # is value in setted bounds with ACC delta
    if value <= bounding + ACC and value >= bounding - 2:
        return True
    else:
        return False

def slide_at_angle(angle):
    img = get_window_image(handle)
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    _, curr_a = current_angle(img)
    print(in_bounds(curr_a, angle))
    dx = SLIDE_DELTA if curr_a < angle else -SLIDE_DELTA
    while in_bounds(curr_a, angle) == False:
        slide(x, y, x + dx, y, handle)
        img = get_window_image(handle)
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        _, curr_a = current_angle(img)
        # time.sleep(0.001)
    print('Final Angle', curr_a)

def sight_roi(img):
    return img[50 + 1:308 - 2, 1024 + 3:1286 - 3] # change for diff resolution


def current_angle(img):
    mini_map = sight_roi(img)
    return camera_angle(mini_map)
# Read image
ANGLE = 180
# while True:
img = get_window_image(handle)
slide_at_angle(ANGLE)
