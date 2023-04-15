import time
import threading

import cv2
from numpy import char
from win32 import win32gui as w

import config
from driver import click, press, slide,send
from screen_reader import get_window_image
from ocr import get_numbers_from_img, get_char_name
from utils.deep_utils import draw_grid, get_active_windows

from enhancer.invetory_dispatcher import InventoryDispatcher
from exam import detect

CONFIG_FILE = 'config.yml'
STATE_FILE = 'state.yml'
CFG = config.load_config(CONFIG_FILE)
state = config.load_config(STATE_FILE)
NUMBERS_AREA = (890, 290, 45, 25)
working = True

def get_window_coord(whandle):
    rect = w.GetWindowRect(whandle)
    l,t, r,b = rect
    x = int((r-l)/2)
    y = int((b-t)/2)
    return x, y

def farming(*args):
    whandle = args[0]['handle']
    char_name = args[0]['name']
    x, y = get_window_coord(whandle)

    while working:
        # time.sleep(1)
        press(whandle, '1')
        time.sleep(0.5)
        press(whandle, '1')
        time.sleep(0.5)
        press(whandle, '1')
        time.sleep(0.5)
        press(whandle, '1')
        time.sleep(0.5)
        press(whandle, '2')
        check_numbers(whandle, char_name)
        slide(x, y, x + 90, y, whandle)

def necro(*args):
    whandle = args[0]['handle']

    while working:
        time.sleep(1)
        press(whandle, '1')
        time.sleep(1)
        press(whandle, '2')


def wind(*args):
    whandle = args[0]['handle']

    while working:
        click(1180, 473 - 25, whandle)
        # click(1250, 455 - 25, whandle)

        time.sleep(1)
        press(whandle, '1')
        time.sleep(24)
        click(1250, 473 - 25, whandle)

        time.sleep(1)
        press(whandle, '1')
        time.sleep(24)


def check_numbers(handle, name):
    img = get_window_image(handle)
    detect(img, handle, name)

def start(**kwargs):
    whandles = get_active_windows(CFG['whandle'])
    print(state)
    for hwnd in whandles:
        t = None
        if hwnd != 0:
            char_name = get_char_name(get_window_image(hwnd))
            print('PID, Char: ', str(hwnd), char_name)
            if char_name in state['farmers']:
                t = threading.Thread(target=farming, args=(hwnd,))
                
        if t:
            time.sleep(2)
            t.start()

if __name__ == "__main__":
    start()
