import numpy as np
import cv2
from win32 import win32gui as api
import win32ui as ui
from win32.lib import win32con as con
from win32 import win32api
import time
def get_window_coord(whandle):
	print(whandle)
	rect = api.GetWindowRect(whandle)
	l,t,r,b = rect
	w = r - l
	h = b - t
	return l, t, w, h

def get_active_windows(handle):
	process_whandles = []
	
	def handleWindow(hwnd, ctx):
	    if api.GetWindowText(hwnd) == 'Rappelz':
	        process_whandles.append(hwnd)
	        

	api.EnumWindows(handleWindow, None)
	print(process_whandles)
	return process_whandles



hwnd = get_active_windows('Rappelz')[0]
# # hwnd = api.GetDesktopWindow()

# api.SetActiveWindow(hwnd)
# api.SetForegroundWindow(hwnd)
def get_window_image(hwnd):
	roi = get_window_coord(hwnd)
	width = roi[0] + roi[2]
	height = roi[1] + roi[3]
	wdc = api.GetWindowDC(hwnd)
	srcdc = ui.CreateDCFromHandle(wdc)
	memdc = srcdc.CreateCompatibleDC()
	bmp = ui.CreateBitmap()
	print(roi)
	bmp.CreateCompatibleBitmap(srcdc, width, height)
	memdc.SelectObject(bmp)
	memdc.BitBlt((0, 0), (width, height), srcdc, (0,0), con.SRCCOPY)
	signedInts = bmp.GetBitmapBits(True)
	# cv2 magic
	img = np.fromstring(signedInts, dtype='uint8')
	img.shape = (height, width, 4)
	srcdc.DeleteDC()
	memdc.DeleteDC()
	api.ReleaseDC(hwnd, wdc)
	api.DeleteObject(bmp.GetHandle())


	cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
	return img

start = time.time()
# i = get_window_image(hwnd)
# end = time.time() - start
# print('time to end ', end)
# # print(img.shape)
# cv2.imwrite('img2.png', i)