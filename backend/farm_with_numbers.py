import time
import threading
# from logging_config import setup_logging
import logging
import cv2
from numpy import char
from win32 import win32gui as w

import config
from driver import click, pclick, press, slide, send, double
from screen_reader import get_window_image
from ocr import get_numbers_from_img, get_char_name, get_numbers
from utils.deep_utils import draw_grid, get_active_windows
from world_explorer.utils import find_npc

from jobs.helpers.extruder import Extruder
from enhancer.invetory_dispatcher import InventoryDispatcher

from exam_v2 import detect

logger = logging.getLogger(__name__)

WEIGHT_MARKER = 'assets/weight_marker.png'
WEIGHT_TRESHOLD = 10# 74
FEATHER_BACK_KEY = '9'
FEATHER_RETURN_KEY = '0'
HELPER_NPC = 'assets/helper_npc.png'

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
    logger.info('Farming started with: {0}'.format(args))
    whandle = args[0]['handle']
    char_name = args[0]['name']
    t = threading.Thread(target=check_numbers, args=(whandle, char_name,))
    t.start()
    # while True:
        # fight(whandle)
        # time.sleep(0.2)
    # sell_action(args[0])
    sell(whandle)


def fight(whandle):
    x, y = get_window_coord(whandle)
    working = 0
    while working < 200:
        # time.sleep(1)
        for i in range(15):
            press(whandle, '1')
            time.sleep(0.3)
            # press(whandle, '1')
            # time.sleep(0.3)
            # press(whandle, '1')
            # time.sleep(0.3)
            # press(whandle, '1')
            # time.sleep(0.3)
            # press(whandle, '1')
            # time.sleep(0.3)
            # press(whandle, '2')

        slide(x, y, x + 200, y, whandle)
        press(whandle, 'tab')
        press(whandle, '3')
        time.sleep(0.3)
        press(whandle, '4')
        time.sleep(0.3)
        press(whandle, '5')
        time.sleep(0.3)
        working = working + 1

def sell_action(cfg):
    logger.info('Sell action started with: {0}'.format(cfg))
    handle = cfg['handle']
    img = get_window_image(handle)
    marker = cv2.imread(WEIGHT_MARKER)
    e = Extruder(img)
    res = e.match_by_template(marker, method='threshold')
    if res is not None:
        logger.debug('Weight marker found: {0}'.format(res))
        x, y, w, h = res
        weight_roi = img[y:y+h, x+w:x+w+25]
        weight = get_numbers(weight_roi)
        if int(weight) > WEIGHT_TRESHOLD:
            logger.debug('Weight is more than {0} - selling'.format(WEIGHT_TRESHOLD))
            press(handle, FEATHER_BACK_KEY)
            time.sleep(6)
            logger.debug('Returning to the farm')
        else:
            logger.debug('Weight is less than {0} - not selling'.format(WEIGHT_TRESHOLD))
    # cv2.imshow('Image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

def sell(handle):
    _step_to_helper_npc(handle)

def _step_to_helper_npc(handle):
    img = get_window_image(handle)
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    # Moving to npc
    x, y = find_npc(img, npc=HELPER_NPC)
    logger.info('NPC found at: {0}, {1}'.format(x, y))
    click(x, y, handle)
    time.sleep(0.1)
    click(x, y, handle)
    time.sleep(2)

    img = get_window_image(handle)
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    # Moving to npc
    x, y = find_npc(img, npc=HELPER_NPC)
    logger.info('NPC found at: {0}, {1}'.format(x, y))
    click(x, y, handle)
    time.sleep(0.1)
    click(x, y, handle)
    time.sleep(2)

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

def support(handle):
    # send(handle, '1')
    pclick((460, 330 - 25), handle)
    time.sleep(0.5)

    for i in range(5):
        pclick((370, 610 - 25), handle)
        time.sleep(0.4)
    
    pclick((540, 330 - 25), handle)
    time.sleep(0.5)

    pclick((597, 605 - 25), handle)
    time.sleep(0.5)

    for i in range(5):
        pclick((370, 530 - 25), handle)
        time.sleep(0.4)

    double(30, 300 - 25, handle)
    time.sleep(3)
    
    PET_POINT = (135, 130 - 25)
    pclick(PET_POINT, handle)
    time.sleep(0.5)

    press(handle, '2')
    time.sleep(0.5)

def wind(*args):
    whandle = args[0]['handle']

    while working:
        click(1180, 291 - 25, whandle)
        # click(1250, 455 - 25, whandle)

        time.sleep(1)
        press(whandle, '1')
        # support(whandle)
        time.sleep(24)
        click(1250, 291 - 25, whandle)

        time.sleep(1)
        press(whandle, '1')
        # support(whandle)
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
                