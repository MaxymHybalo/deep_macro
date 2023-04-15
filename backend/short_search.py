from screen_reader import get_window_image
from driver import press
import sys
import os
import cv2
import numpy as np
import time

def find_skill(img):
    
    template = cv2.imread('C:/uo_images/search_half.png')
    # half = cv2.imread('C:/uo_images/search_half.png')
    # cv2.imshow('2', template);cv2.waitKey(0)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    print(template.shape)
    w,h = (10, 18)
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    threshold = .8
    loc = np.where(res >= threshold)
    print(loc[0])
    if len(loc[0]) == 0:
        return False
    else:
        # cv2.imshow('result.png', img)
        # cv2.waitKey(0)
        return True

    # for pt in zip(*loc[::-1]):  # Switch collumns and rows
    #     cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    # cv2.imshow('result.png', img)
    # cv2.waitKey(0)
    return True

if __name__ == '__main__':
    print(sys.argv)
    _, h, key = sys.argv
    handle = int(h)
    try:
        print(os.path.dirname(os.path.abspath(__file__)))

        img = get_window_image(handle)
        x = find_skill(img)
        if not x:
            press(h, key)
            time.sleep(0.1)
            press(h, key)
            time.sleep(0.1)
            press(h, key)


        print('end exec')
    except:
        print('error')


