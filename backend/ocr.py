from threading import main_thread
from pip import main
import pytesseract
import cv2
import numpy as np
from datetime import datetime

ALPHABET = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz.'
# ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
NUMBERS_AREA = (730, 290, 45, 25)
CHARNAME_AREA = (45, 28, 170, 16)
def crop_roi(img, roi):
    x,y, w,h = roi
    return img[y:y+h, x:x+w]


def pre_process_number_reading(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, th1 = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
    img = th1
    return img


def _prepare_recognizing(img, roi, thresholding=True):
    if img is None:
        return None
    img = crop_roi(img, roi)
    if thresholding:
        img = pre_process_number_reading(img)
    return img


def get_numbers_from_img(img, handle=0):
    img = _prepare_recognizing(img, NUMBERS_AREA)
    # change lang  to specified
    try:
        text = pytesseract.image_to_string(img, config='-c tessedit_char_whitelist=0123456789')
    except:
        print('ERROR IMAGE', img)
        return None
    text = ''.join(text.strip())
    text = text[:3]
    if len(text) > 0:
        imname = str(handle) + '_' + str(datetime.now().strftime('%H_%M_%S')) + '.png'
        print('logs to: ', imname, img.shape)
        cv2.imwrite('logs/' + imname, img)
    print('Tesseract text extracted: ', text, 'length', len(text))
    return text if len(text) == 3 else None


def get_char_name(img):
    img = _prepare_recognizing(img, CHARNAME_AREA, False)
    text = pytesseract.image_to_string(img, config='-c tessedit_char_whitelist=' + ALPHABET)
    text = ''.join(text.strip())
    print('Tesseract Charname extracted: ', text, len(text))
    return text


def get_numbers(img, char_list='0123456789'):
    return pytesseract.image_to_string(img, config='--oem 2 -c tessedit_char_whitelist={0}'.format(char_list), lang='rus')

def get_text(img, lang='rus'):
    res = pytesseract.image_to_string(img, lang=lang)
    res = ' '.join(res.split())
    return res

def _awaking_rect(points, i):
    sx, sy, dx, width, height = points
    return (sx + width*i + i*dx, sy, width, height)

def get_awaking(img = None):
    if img is None:
        img = cv2.imread('logs/awaking/awake_16_30_05_03_05_22.png')

    prop_location = (3, 4, 7, 73, 44)
    value_location = (23, 50, 45, 35, 22)

    results = []
    for i in range(5):
        char_roi = crop_roi(img, _awaking_rect(prop_location,i))
        char_roi = cv2.cvtColor(char_roi, cv2.COLOR_BGR2GRAY)
        ret, th1 = cv2.threshold(char_roi, 78, 255, cv2.THRESH_BINARY)
        char_roi = th1
        # cv2.imwrite('logs/awaking/prop_{}.png'.format(i), char_roi)
        res = pytesseract.image_to_string(char_roi, lang="rus")
        res = ' '.join(res.split())

        value_roi = crop_roi(img, _awaking_rect(value_location, i))
        default_number_search = '-c tessedit_char_whitelist=0123456789+'
        v = pytesseract.image_to_string(value_roi, config=default_number_search)
        # cv2.imshow('Image', value_roi)
        # cv2.waitKey(0)
        v = ''.join(v.strip())
        if len(v) == 0:
            single_digit_search = '--psm 10'
            value_roi = crop_roi(value_roi, (17, 0, 19, 22))
            v = pytesseract.image_to_string(value_roi, config=single_digit_search)

        # cv2.imwrite('logs/awaking/value_{}__{}.png'.format(i, str(datetime.now().strftime('%H_%M_%S'))), value_roi)
        v = ''.join(v.strip())

        # print(i, res, v)
        results.append((i, res, v))
    # print(results)
    return results

if __name__ == '__main__':
    get_awaking()