import os
import time
import cv2

import sys
print(sys.path, os.getcwd())
sys.path.insert(0, os.getcwd())

from screen_reader import get_window_image


FILE_PATH = 'logs/world_explorer'

def record(handle):
    counter = 0
    while True:
        img = get_window_image(handle)
        img = img[50 + 1:308 - 2, 1024 + 3:1286 - 3]
        _save(img, str(counter))
        time.sleep(0.1)
        counter = counter + 1

def _save(img, name):
    print('try to save')
    cv2.imwrite('{}/{}.png'.format(FILE_PATH, name), img)


if __name__ == '__main__':
    handle = 656458 # handle
    record(handle)