import time
import threading	

import cv2
from win32 import win32gui as w

import config
from driver import click, press, slide,send
from screen_reader import get_window_image
from numbers_validate import get_numbers_from_img
import open_cards_job

from enhancer.invetory_dispatcher import InventoryDispatcher

CONFIG_FILE = 'config.yml'
CFG = config.load_config(CONFIG_FILE)
NUMBERS_AREA = (890, 290, 80, 30)

# whandle = w.FindWindow(None, CFG['whandle']) 

def get_active_windows(handle):
	process_whandles = []
	
	def handleWindow(hwnd, ctx):
	    if w.GetWindowText(hwnd) == 'Rappelz':
	        process_whandles.append(hwnd)
	        
	w.EnumWindows(handleWindow, None)
	print(process_whandles)
	return process_whandles

def get_window_coord(whandle):
	rect = w.GetWindowRect(whandle)
	l,t, r,b = rect
	x = int((r-l)/2)
	y = int((b-t)/2)
	return x, y

def simple_farm(*args):
	whandle = args[0]
	print(args)
	notify = None
	x, y = get_window_coord(whandle)

	while True:
		press(whandle, '2')
		time.sleep(2.5)
		press(whandle, '1')
		time.sleep(1)
		press(whandle, '1')
		time.sleep(1)
		check_numbers(whandle, notify)
		slide(x, y, x + 45, y, whandle)

def check_numbers(handle, notify):
	img = get_window_image(handle)
	x, y, w, h = NUMBERS_AREA
	cv2.rectangle(img, (x, y), (x + w, y + h), (255,0,0), 2)
	cv2.imwrite('logs/' + str(handle) + '.png', img)
	numbers = get_numbers_from_img(img, handle=handle)

	if numbers:
		# notify(hwnd=handle, data=numbers)
		send(handle, numbers)

def configure(handle):
	return InventoryDispatcher('enhancer.config.yml', handle)

def polling(**kwargs):
	time.sleep(1)

	whandles = get_active_windows(CFG['whandle'])
	
	# handle = whandles[0]
	
	# print(numbers)

	for hwnd in whandles:
		t = None
		# if hwnd == 2820856:
		# from taming import taming
			# t = threading.Thread(target=taming, args=(hwnd,))
		# t = threading.Thread(target=open_cards_job.open, args=(hwnd,))
		# if hwnd != 1969744:
		# if hwnd != 2820856:
		if hwnd != 0:
			print('breakpoint')
			# inventory = configure(hwnd)
			# t = threading.Thread(target=inventory.enhance, args=(hwnd,))
			t = threading.Thread(target=simple_farm, args=(hwnd,))
		if t:
			time.sleep(2)
			t.start()


if __name__ == "__main__":
	polling()	
