import os
import time
import re
import cv2
from datetime import datetime
import numpy as np
from random import randint, random
from screen_reader import get_window_image
from driver import click
from ocr import get_text, get_numbers
from utils.awaking_aggregator import levenshtein_ratio_and_distance
from jobs.helpers.extruder import Extruder

DEV_MODE = True
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 768
# colors
COLOR_CANCEL = (200, 0, 0)
COLOR_CAPCHA_ROI = (10, 200, 0)
COLOR_OPTION = (20, 20, 200)
COLOR_RESULT = (100, 30, 100)
# EXAMPLE = 'new_capcha.png'
EXAMPLE = 'test_2.jpg'
DECLIHE_EXAM = 'assets/decline_exam.png'

C_WIDTH = 318
C_HEIGHT = 218
CAPCHA_ROI = (482, 301, C_WIDTH, C_HEIGHT) # centralize captcha

SEARCHING_AREA = (475, 265, C_WIDTH + 14, C_HEIGHT + 75)
EXAM_HEIGHT = 28

OPTIONS_START = (36, 38)
OPTION_SHAPE = (249, 28)

img = None


def _crop(img, roi=CAPCHA_ROI):
    x,y,w,h = roi
    # return img[CAPCHA_ROI[1]:CAPCHA_ROI[1] + CAPCHA_ROI[3], CAPCHA_ROI[0]:CAPCHA_ROI[0] + CAPCHA_ROI[2]]
    return img[y:y+h, x:x+w]


def gen_options_matrix():
    res = []
    w,h = OPTION_SHAPE
    x, y = OPTIONS_START
    for o in range(5):
        res.append([x, y + h*o])
    return res

def detect(img, handle, name):
    originImg = np.copy(img)
    if isinstance(img, type(None)):
        print(img)
        return
    
    originImg = img
    res, img = _find_exam_window(_crop(img, roi=SEARCHING_AREA), file=name)
    
    # print('exam pointer', res)
    if res is None:
        return

    img = _crop(originImg)
    # cv2.imshow('Image', img)
    # cv2.waitKey(0)
    
    if DEV_MODE:
        cv2.rectangle(originImg, (CAPCHA_ROI[0], CAPCHA_ROI[1]), (CAPCHA_ROI[0] + C_WIDTH, CAPCHA_ROI[1] + C_HEIGHT), [100, 0, 100], 1)

    exam_row = img[0:EXAM_HEIGHT, 0:C_WIDTH]

    text = get_text(exam_row)
    if not len(text):
        _save(originImg, '{}_original'.format(name), handle)
        return
    value = re.findall('[0-9]+', text)
    value = value[0] if len(value) > 0 else None
    print('[value, text]', value, text)

    options = gen_options_matrix()
    resulted = -1

    for i, o in enumerate(options):
        x, y = o
        w,h = OPTION_SHAPE
        if DEV_MODE:
            cv2.rectangle(img, (x, y), (x + w, y+h), COLOR_OPTION, 1)
        
        opt_img = img[y:y+h, x:x+w] 
        opt_img = cv2.cvtColor(opt_img, cv2.COLOR_BGR2GRAY)
        ret, th1 = cv2.threshold(opt_img, 160, 255, cv2.THRESH_BINARY)
        # cv2.putText(opt_img, 'Мокд текст', (x, y+h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0, 190, 200], 1)
        opt_value = get_numbers(th1)
        if not len(opt_value):
            scale_percent = 220 # percent of original size
            width = int(th1.shape[1] * scale_percent / 100)
            height = int(th1.shape[0] * scale_percent / 100)
            dim = (width, height)
            
            # resize image
            resized = cv2.resize(opt_img, dim, interpolation = cv2.INTER_AREA)
            ret, th1 = cv2.threshold(resized, 110, 255, cv2.THRESH_BINARY)
            kernel = np.ones((1,1), np.uint8)

            # th1 = cv2.erode(th1, kernel, iterations=1)
            opt_value = get_numbers(th1)
            # cv2.imshow('Image', th1)
            # cv2.waitKey(0)

        opt_value= opt_value.strip()
        # print(opt_value)
        if opt_value == value:
            if DEV_MODE:
                cv2.circle(img, (x + int(w/2), y + int(h/2)), 3, COLOR_RESULT, 2)
            resulted = i
            print('[FINDED] ', i)

    if resulted == -1:
        _save(originImg, '{}_original'.format(name), handle)
        return

    ax, ay = options[resulted]
    opt_w, opt_h = OPTION_SHAPE
    print('CAPCHA_ROI[0:1]', CAPCHA_ROI[0:2])
    ox, oy = CAPCHA_ROI[0:2]
    ox, oy = ox + ax + int(opt_w / 2), oy + ay - 25 + int(opt_h / 2)
    cv2.circle(originImg, (ox, oy), 3, COLOR_OPTION, -1)
    _save(originImg, name, handle)

    time.sleep(2 + randint(1, 2))
    click(ox, oy, handle)
    time.sleep(0.5)
    click(ox, oy, handle)

    print('[CLICKED AT OPTION]', resulted)

def _find_exam_window(img, file=''):
    template = cv2.imread(DECLIHE_EXAM)
    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(grayImage, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    loc = list(zip(*loc[::-1]))
    if not len(loc):
        return None, img
    x, y = loc[0]
    h, w = template.shape
    # print('matchTemplate loc', loc, file)
    cv2.rectangle(img, (x,y), (x + w, y + h), (122, 0,244), 2)

    return (x, y, w, h), img

def _save(img, name, handle):
    date = datetime.now().strftime('%H_%M_%S_%d_%m_%y')
    try:
        os.mkdir('logs/{}'.format(name))
    except FileExistsError:
        pass
    cv2.imwrite('logs/{}/{}_{}.png'.format(name, str(handle), date), img)

if __name__ == '__main__':
    # RESOURCES = 'logs/captcha_examples'
    # files = os.listdir(RESOURCES)

    # for f in files:
        # img = cv2.imread('{}/{}'.format(RESOURCES, f))
    img = cv2.imread(EXAMPLE)

    detect(img, 12421451, 'test')