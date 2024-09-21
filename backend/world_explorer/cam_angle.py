import cv2
import numpy as np
import sys,os
import time

sys.path.insert(0, os.getcwd())

from screen_reader import get_window_image
from driver import click, double, slide, press
from angle import camera_angle
from world_explorer.utils import window_center, levenshtein_ratio_and_distance
from ocr import get_text

handle = 1051262
x, y = window_center(handle)
ACC = 2 # how accurate angle
SLIDE_DELTA = 4
BOSSES = {
    'first': 'Хранитель врат'
}

def in_bounds(value, bounding): # is value in setted bounds with ACC delta
    if value <= bounding + ACC and value >= bounding - 2:
        return True
    else:
        return False

def slide_at_angle(angle):
    img = get_image(handle)
    _, curr_a = current_angle(img)
    print(in_bounds(curr_a, angle))
    dx = SLIDE_DELTA if curr_a < angle else -SLIDE_DELTA
    while in_bounds(curr_a, angle) == False:
        slide(x, y, x + dx, y, handle)
        img = get_image(handle)
        _, curr_a = current_angle(img)
        # time.sleep(0.001)
    print('Final Angle', curr_a)

def move_forward():
    click(x, y - 100, handle)
    time.sleep(0.8)

def sight_roi(img):
    return img[50 + 1:308 - 2, 1024 + 3:1286 - 3] # change for diff resolution

def get_image(handle):
    img = get_window_image(handle)
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    return img

def current_angle(img):
    mini_map = sight_roi(img)
    return camera_angle(mini_map)

def fight():
    print('Start Fight')
    while True:
        press(handle, '1')
        time.sleep(0.1)
        press(handle, '2')
        time.sleep(0.1)
        press(handle, '3')
        time.sleep(0.1)

def find_target(name):
    press(handle, 'tab')
    time.sleep(0.1)
    img = get_image(handle)
    target_name_roi = img[25 + 1:49, 670:800]
    target_name_roi = cv2.cvtColor(target_name_roi, cv2.COLOR_BGR2GRAY)
    text = get_text(target_name_roi)
    print(text)
    ratio = 0
    if text:
        ratio = levenshtein_ratio_and_distance(text, name, ratio_calc=True)
    print(ratio)
    if ratio > 0.8:
        fight()
    else:
        press(handle, 'tab')
        find_target(name)
    
# Read image
ANGLE = 313.7
# while True:

# slide_at_angle(ANGLE)
img = get_image(handle)

# move to 1 boss
for i in range(20):
    slide_at_angle(325.0)
    move_forward()
# find boss

# slide_at_angle(330.5)
# for i in range(5):
#     move_forward()
find_target(BOSSES['first'])
print(current_angle(img))
# img = sight_roi(img)
# idk(img)