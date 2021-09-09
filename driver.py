from win32 import win32gui as w
from win32.lib import win32con as con
from win32 import win32api
import time

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
}

def press(whandle, key):
	w.PostMessage(whandle, con.WM_KEYDOWN, KEYS[key])
	w.PostMessage(whandle, con.WM_KEYUP, KEYS[key])
# WM_LBUTTONDOWN

def click(x, y, whandle):
	point = win32api.MAKELONG(x, y)
	w.PostMessage(whandle, con.WM_LBUTTONDOWN, 0, point)
	w.PostMessage(whandle, con.WM_LBUTTONUP, 0, point)

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

# press(460616, '1')
