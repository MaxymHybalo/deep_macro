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


def _awaking_rect(points, i):
    sx, sy, dx, width, height = points
    return (sx + width*i + i*dx, sy, width, height)

def get_awaking(img = None):
    img = cv2.imread('logs/awaking/awaket_00_39_09_$d_$m_$Y.png')
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
        res = ''.join(res.strip())
        value_roi = crop_roi(img, _awaking_rect(value_location, i))
        # cv2.imwrite('logs/awaking/value_{}.png'.format(i), value_roi)
        v = pytesseract.image_to_string(value_roi, config='-c tessedit_char_whitelist=0123456789+')
        v = ''.join(v.strip())
        print(i, res, v)
        results.append((i, res, v))
    print(results)
    return results

if __name__ == '__main__':
    get_awaking()