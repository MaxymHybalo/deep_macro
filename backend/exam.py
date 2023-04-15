import os
import time
import re
import cv2
from datetime import datetime
import numpy as np
from random import randint, random
from screen_reader import get_window_image
from driver import click
from ocr import get_text
from utils.awaking_aggregator import levenshtein_ratio_and_distance
from jobs.helpers.extruder import Extruder

DEV_MODE = True
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 768
# colors
COLOR_CANCEL = (200, 0, 0)
COLOR_CAPCHA_ROI = (10, 200, 0)
COLOR_OPTION = (20, 20, 200)
EXAMPLE = 'assets/example4.png'
EXAM_WND = 'assets/exam_window.png'
C_WIDTH = 305
C_HEIGHT = 44
CAPCHA_ROI = (230, 210, C_WIDTH, C_HEIGHT) # centralize captcha
COMPARE_TEXT = 'Вы! робот? Введите номер 000'

DIAL_ROI = (57, 76)
DIAL_POINT = (692, 379)

DIAL_MAP = [9, 6, 7, 8, 3, 4, 5, 0, 1, 2]
img = cv2.imread(EXAMPLE)

def _crop(img):
    return img[CAPCHA_ROI[1]:CAPCHA_ROI[1] + CAPCHA_ROI[3], CAPCHA_ROI[0]:CAPCHA_ROI[0] + CAPCHA_ROI[2]]

def detect(img, handle, name):
    originImg = np.copy(img)
    if isinstance(img, type(None)):
        print(img)
        return 
    img = _crop(img)
    if DEV_MODE:
        cv2.rectangle(originImg, (CAPCHA_ROI[0], CAPCHA_ROI[1]), (CAPCHA_ROI[0] + C_WIDTH, CAPCHA_ROI[1] + C_HEIGHT), [100, 0, 100], 1)

    text = get_text(img)
    print(text)
    if not len(text):
        return
    ratio = levenshtein_ratio_and_distance(text, COMPARE_TEXT, ratio_calc=True)
    value = re.findall('[0-9]+', text)
    value = value[0] if len(value) > 0 else None
    print('value, text, ratio', value, text, ratio)

    if value and ratio > 0.7:
        time.sleep(6 + randint(1, 4)) # add some correction
        exam_roi, img = _find_exam_window(originImg)
        ex, ey, ew, eh = exam_roi
        originImg = img
        if ex > 1:
            dial_img, dial = get_dial(originImg)
            originImg = dial_img
            originImg = insert_exam(handle, value, dial, img=originImg)


            ok_x = 650 + randint(-20, 20)
            ok_y = 445 - 25 + randint(-5, 5)
            cv2.circle(originImg, (ok_x, ok_y), 2, (0, 200, 0), 1)
            delay = 1 + 1 / randint(2, 5)
            time.sleep(delay)
            print('try to click ok', delay, ok_x, ok_y)
            click(ok_x, ok_y, handle)
            _save(originImg, name, handle)

    # cv2.imshow('Image', originImg)
    # cv2.waitKey(0)

def insert_exam(handle, value, dial, img=None):
    digits = [int(i) for i in str(value)]
    print(digits)

    for d in digits:
        x, y = dial[d]
        px = x + 8 + randint(-5, 5)
        py = y + 8 + randint(-5, 5)

        cv2.circle(img, (px, py), 2, [10, 10, 234], 1)

        delay = 1 / randint(1, 4) + 1 / randint(6, 20)
        time.sleep(delay)
        # print(delay)
        click(px, py - 25, handle)
    return img
    # cv2.imshow('Image', img)
    # cv2.waitKey(0)
    
def get_dial(img):
    w, h = DIAL_ROI
    x,y = DIAL_POINT
    dial = []
    dial_map = []
    counter = 0
    for row in range(4):
        for col in range(3):
            dy = row*16 + y + 3*row
            dx = col*16 + x + 4*col
            cv2.rectangle(img, (dx, dy), (dx+16, dy+16), (255, 0,244), 1)
            if counter not in [9, 11]:
                cv2.putText(img, str(counter), (dx + 3 + w + 10, dy + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0, 190, 200], 1)
                dial.append((dx, dy))
            counter = counter + 1

    for i in DIAL_MAP:
        dial_map.append(dial[i])

    for i, p in enumerate(dial_map):
        cv2.putText(img, str(i), (p[0] + 3 , p[1] + 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [250, 190, 200], 1)

    return img, dial_map

def _find_exam_window(img):
    res = Extruder(img).match_by_template(cv2.imread(EXAM_WND))
    x, y, w, h = res

    cv2.rectangle(img, (x,y), (x + w, y + h), (122, 0,244), 2)
    # cv2.imshow('Image', img)
    # cv2.waitKey(0)
    return res, img

def _save(img, name, handle):
    date = datetime.now().strftime('%H_%M_%S_%d_%m_%y')
    print('try to save')
    try:
        os.mkdir('logs/{}'.format(name))
    except FileExistsError:
        print('logs path created')
    cv2.imwrite('logs/{}/{}_{}.png'.format(name, str(handle), date), img)

# from win10toast import ToastNotifier

# toast = ToastNotifier()

# toast.show_toast(
#     "Notification",
#     "Notification body",
#     duration = 20,
#     icon_path = "icon.ico",
#     threaded = True,
# )

if __name__ == '__main__':
    detect(img, 12421451, 'test1')