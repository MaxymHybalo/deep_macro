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

from jobs.helpers.extruder import Extruder
from enhancer.invetory_dispatcher import InventoryDispatcher

from exam_v2 import detect

CONFIG_FILE = 'config.yml'
STATE_FILE = 'state.yml'
CFG = config.load_config(CONFIG_FILE)
state = config.load_config(STATE_FILE)
NUMBERS_AREA = (890, 290, 45, 25)
working = True

LUNA = 'assets/luna_marker.png'
SEARCH_TEMPLATE = 'assets/search.png'
FEATHER_TEMPLATE = 'assets/feather.png'
INVENTORY_CONFIG = 'enhancer.config.yml'
OL_DELAY = 0.3
LEADER_KEY = 'f2'

def get_window_coord(whandle):
    rect = w.GetWindowRect(whandle)
    l,t, r,b = rect
    x = int((r-l)/2)
    y = int((b-t)/2)
    return x, y

def farming(*args):
    print('[args]', args)
    whandle = args[0]['handle']
    char_name = args[0]['name']
    t = threading.Thread(target=check_numbers, args=(whandle, char_name,))
    t.start()
    while True:
        fight(whandle)
        time.sleep(1)
        keeper(args[0])


def fight(whandle):
    x, y = get_window_coord(whandle)
    working = 0
    while working < 200:
        # time.sleep(1)
        for i in range(1):
            press(whandle, '1')
            time.sleep(0.5)
            press(whandle, '1')
            time.sleep(0.5)
            press(whandle, '1')
            time.sleep(0.5)
            press(whandle, '1')
            time.sleep(0.5)
            press(whandle, '1')
            time.sleep(0.5)
            press(whandle, '2')

        slide(x, y, x + 200, y, whandle)
        press(whandle, 'tab')
        press(whandle, '3')
        time.sleep(0.5)
        press(whandle, '4')
        time.sleep(0.5)
        press(whandle, '5')
        time.sleep(0.5)
        working = working + 1

def keeper(cfg):
    inventory = InventoryDispatcher(INVENTORY_CONFIG, cfg)
    inventory.keeper()

def necro(*args):
    handle = args[0]['handle']
    luna = cv2.imread(LUNA)
    search = cv2.imread(SEARCH_TEMPLATE)
    feather = cv2.imread(FEATHER_TEMPLATE)


    def trigger_present(img, template, rect):
        if isinstance(img, type(None)):
            print('[NO IMAGE]')
            return False
        e = Extruder(img)
        # print('extruder', e)
        res = e.match_by_template(template, method='threshold')
        rx, ry, rxe, rye = rect
        if res:
            x, y, _, _ = res
            print('[LUNA RES]', res)

            if x >= rx and x <= rxe:
                return True
        return False
    search_phase = 0
    while working:
        press(handle, LEADER_KEY)
        time.sleep(0.2)
        press(handle, '1')
        time.sleep(0.2)
        # find image
        img = get_window_image(handle)
        # e = Extruder(img)
        # res = e.match_by_template(luna, method='threshold')

        if trigger_present(img, luna, (400, 0, 790, 0)):
            press(handle, '2')
            time.sleep(OL_DELAY)
            press(handle, '3')
            time.sleep(OL_DELAY)
            press(handle, '4')
            time.sleep(OL_DELAY)
            press(handle, '5')
            time.sleep(OL_DELAY)
            press(handle, '6')
            if trigger_present(img, search, (400, 0, 790, 0)) == False:
                print('search trigger')
                time.sleep(OL_DELAY)
                press(handle, '9' if search_phase == 0 else '0')
                search_phase = 1 if search_phase == 0 else 1
            # if trigger_present(img, search, (400, 0, 790, 0)) == False:
            #     time.sleep(OL_DELAY)
            #     press(handle, '0')
        if trigger_present(img, feather, (630, 0, 750, 0)):
            time.sleep(OL_DELAY)
            click(685, 450 - 25, handle)
            
def wind(*args):
    whandle = args[0]['handle']

    while working:
        click(1180, 614 - 25, whandle)
        # click(1250, 455 - 25, whandle)

        time.sleep(1)
        press(whandle, '1')
        time.sleep(24)
        click(1250, 614 - 25, whandle)

        time.sleep(1)
        press(whandle, '1')
        time.sleep(24)


def check_numbers(handle, name):
    while working:
        img = get_window_image(handle)
        detect(img, handle, name)
        time.sleep(0.5)
        # print('[EXAM TICK]')

# def start(**kwargs):
#     whandles = get_active_windows(CFG['whandle'])
#     print(state)
#     char_name = get_char_name(get_window_image(hwnd))
#     if hwnd != 0:
#         for hwnd in whandles:
#             t = None
#             print('PID, Char: ', str(hwnd), char_name)
#             if char_name in state['farmers']:
#                 t = threading.Thread(target=farming, args=(hwnd,))
                