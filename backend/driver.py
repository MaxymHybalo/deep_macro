from win32 import win32gui as w
from win32.lib import win32con as con
from win32 import win32api
import time
from utils.deep_utils import get_window_coord, _foreground_window

KEYS = {
    '0': 0x30,
    '1': 0x31,
    '2': 0x32,
    '3': 0x33,
    '4': 0x34,
    '5': 0x35,
    '6': 0x36,
    '7': 0x37,
    '8': 0x38,
    '9': 0x39,
    'tab': 0x09,
    'f1': 0x70,
    'f2': 0x71,
    'f3': 0x72,
    'f4': 0x73,
    'f5': 0x74,
    'f6': 0x75,
    'f7': 0x76,
    'f7': 0x77,
    'i': 0x49,
    'l': 0x4c,
    'alt': 0xA5,
    'enter': 0x0D,
    'w': 0x87,
    'v': 0x86,
}

CHAT_FREE_X, CHAT_FREE_Y = (214, 562)

def press(whandle, key):
    w.PostMessage(whandle, con.WM_KEYDOWN, KEYS[key])
    w.PostMessage(whandle, con.WM_KEYUP, KEYS[key])

def alt(whandle, x, y):
    time.sleep(0.1)

    w.PostMessage(whandle, con.WM_KEYDOWN, KEYS['alt'])
    time.sleep(0.1)
    click(x,y, whandle)
    time.sleep(0.1)
    w.PostMessage(whandle, con.WM_KEYUP, KEYS['alt'])
    time.sleep(0.1)

# WM_LBUTTONDOWN

def click(x, y, whandle):
    point = win32api.MAKELONG(x, y)

    w.PostMessage(whandle, con.WM_LBUTTONDOWN, con.MK_LBUTTON, point)
    w.PostMessage(whandle, con.WM_LBUTTONUP, None, point)

def pclick(point, whandle):
    x, y = point
    click(x, y, whandle)


def double(x,y, whandle):

    point = win32api.MAKELONG(x, y)
    w.PostMessage(whandle, con.WM_LBUTTONDBLCLK, con.MK_LBUTTON, point)
    w.PostMessage(whandle, con.WM_LBUTTONUP, None, point)

def move(x, y, trigger, whandle):
    point = win32api.MAKELONG(x, y)
    w.PostMessage(whandle, con.WM_MOUSEMOVE, trigger, point)

def slide(x1, y1, x2, y2, whandle):
    p1 = win32api.MAKELONG(x1, y1)
    p2 = win32api.MAKELONG(x2, y2)
    move(x1, y1, 0, whandle)
    w.PostMessage(whandle, con.WM_RBUTTONDOWN, con.MK_RBUTTON, p2)
    # time.sleep(1)
    move(x2, y2, con.MK_RBUTTON, whandle)

    w.PostMessage(whandle, con.WM_RBUTTONUP, 0, p2)

def drag(x1, y1, x2, y2, whandle):
    p1 = win32api.MAKELONG(x1, y1)
    p2 = win32api.MAKELONG(x2, y2)
    move(x1, y1, 0, whandle)
    w.PostMessage(whandle, con.WM_LBUTTONDOWN, con.MK_LBUTTON, p1)
    time.sleep(1)
    move(x2, y2, con.MK_LBUTTON, whandle)

    w.PostMessage(whandle, con.WM_LBUTTONUP, 0, p2)

def send(whandle, message):

    import pyautogui as u
    import ctypes
    x, y, _, _ = get_window_coord(whandle)
    # print('activate click', x + CHAT_FREE_X, y + CHAT_FREE_Y)
    # ctypes.windll.user32.SetCursorPos(x + CHAT_FREE_X, y + CHAT_FREE_Y)
    _foreground_window(whandle)
    time.sleep(0.2)
    u.press('enter')
    time.sleep(0.1)

    u.write(message, interval=0.1)
    # for m in message:
    #     u.press(m)

    time.sleep(0.1)
    u.press('enter')
    time.sleep(0.2)
    click(CHAT_FREE_X, CHAT_FREE_Y, whandle)

# press(460616, '1')
