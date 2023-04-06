import os
import time
import re
import cv2
import numpy as np
from screen_reader import get_window_image
from driver import click
from ocr import get_text
from utils.awaking_aggregator import levenshtein_ratio_and_distance
from jobs.helpers.extruder import Extruder

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 768
# colors
COLOR_CANCEL = (200, 0, 0)
COLOR_CAPCHA_ROI = (10, 200, 0)
COLOR_OPTION = (20, 20, 200)
# / colors
# EXAMPLE = 'new_capcha.png'
EXAMPLE = 'assets/screen1.png'
EXAM_WND = 'assets/exam_window.png'
C_WIDTH = 305
C_HEIGHT = 72
CAPCHA_ROI = (230, 256, C_WIDTH, C_HEIGHT) # centralize captcha
COMPARE_TEXT = 'Вы! робот? Введите номер 000'

DIAL_ROI = (57, 76)
DIAL_POINT = (692, 379)
img = cv2.imread(EXAMPLE)

# cv2.rectangle(colored, (CAPCHA_ROI[0], CAPCHA_ROI[1]), (CAPCHA_ROI[0] + CAPCHA_ROI[2], CAPCHA_ROI[1] + CAPCHA_ROI[3]), COLOR_CAPCHA_ROI, 2) # capcha
# cv2.rectangle(colored,top_left, bottom_right, COLOR_CANCEL, 2) # cancel rect
# for o in calc_options():
#     x, y = o
#     print(o)
#     cv2.rectangle(colored, (x, y), (x + OPTION_SIZE[0], y + OPTION_SIZE[1]), COLOR_OPTION, 1)
# cv2.imwrite('examp_result.png', colored)
# cv2.imshow('img', colored)
# cv2.waitKey(0)
def _crop(img):
    return img[CAPCHA_ROI[1]:CAPCHA_ROI[1] + CAPCHA_ROI[3], CAPCHA_ROI[0]:CAPCHA_ROI[0] + CAPCHA_ROI[2]]

def detect(img, handle, name):
    originImg = np.copy(img)
    img = _crop(img)
    text = get_text(img)
    ratio = levenshtein_ratio_and_distance(text, COMPARE_TEXT, ratio_calc=True)
    value = re.findall('[0-9]+', text)
    value = value[0] if len(value) > 0 else None
    print('value', value)
    print(text, ratio)
    if value:
        has_exam = _find_exam_window(originImg)
        if has_exam:
            get_dial(originImg)
    # cv2.imshow('Image', img)
    # cv2.waitKey(0)


def get_dial(img):
    w, h = DIAL_ROI
    x,y = DIAL_POINT
    dial = []
    counter = 0
    for row in range(4):
        for col in range(3):
            dy = row*16 + y + 3*row
            dx = col*16 + x + 4*col
            cv2.rectangle(img, (dx, dy), (dx+16, dy+16), (255, 0,244), 1)
            if counter not in [9, 11]:
                cv2.putText(img, str(counter), (dx + 3, dy + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0, 190, 200], 1)
                dial.append((dx, dy))
            counter = counter + 1

    # cv2.imshow('Image', img)
    # cv2.waitKey(0)
    return dial

def _find_exam_window(img):
    res = Extruder(img).match_by_template(cv2.imread(EXAM_WND))
    x, y, _, _ = res

    # cv2.rectangle(img, (x,y), (x+ 100, y+25), (122, 0,244), 2)
    # cv2.imshow('Image', img)
    # cv2.waitKey(0)
    return res[0] > 1
# def _save(img, name, handle):
#     date = datetime.now().strftime('%H_%M_%S_%d_%m_%y')
#     print('try to save')
#     try:
#         os.mkdir('logs/{}'.format(name))
#     except FileExistsError:
#         print('logs path created')
#     cv2.imwrite('logs/{}/{}_{}.png'.format(name, str(handle), date), img)

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