import cv2
import numpy as np
import sys,os
import time

sys.path.insert(0, os.getcwd())

from screen_reader import get_window_image
from driver import click, double
from angle import camera_angle
handle = 1116198
# Read image
while True:
    img = get_window_image(handle)
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    shape = img.shape
    win_h, win_w, _ = shape
    center_w = win_h / 2, win_h / 2

    mini_map = img[50 + 1:308 - 2, 1024 + 3:1286 - 3] # change for diff resolution

    a = camera_angle(mini_map)

    # print('Angle', a)
    time.sleep(0.1)
