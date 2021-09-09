import time
import threading	

import config
from win32 import win32gui as w
from driver import click, press, slide

CONFIG_FILE = 'config.yml'
CFG = config.load_config(CONFIG_FILE)

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
	x, y = get_window_coord(whandle)

	while True:
		for i in range(5):
			press(whandle, '2')
			time.sleep(1)
		slide(x, y, x + 30, y, whandle)



if __name__ == "__main__":
	time.sleep(1)

	whandles = get_active_windows(CFG['whandle'])
		
	for hwnd in whandles:
		t = threading.Thread(target=simple_farm, args=(hwnd,))
		t.start()
