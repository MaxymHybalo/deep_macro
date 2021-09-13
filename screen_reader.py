import numpy as np
import cv2
from win32 import win32gui as api
import win32ui as ui
from win32.lib import win32con as con
from win32 import win32api

def get_window_coord(whandle):
	print(whandle)
	rect = api.GetWindowRect(whandle)
	l,t,r,b = rect
	w = r - l + 1
	h = b - t + 1
	return l, t, w, h

def get_active_windows(handle):
	process_whandles = []
	
	def handleWindow(hwnd, ctx):
	    if api.GetWindowText(hwnd) == 'Rappelz':
	        process_whandles.append(hwnd)
	        

	api.EnumWindows(handleWindow, None)
	print(process_whandles)
	return process_whandles



# hwnd = get_active_windows('Rappelz')[0]
hwnd = api.GetDesktopWindow()
api.SetActiveWindow(hwnd)
api.SetForegroundWindow(hwnd)
roi = get_window_coord(hwnd)
wdc = api.GetWindowDC(hwnd)
srcdc = ui.CreateDCFromHandle(wdc)
memdc = srcdc.CreateCompatibleDC()
bmp = ui.CreateBitmap()
print(roi)
bmp.CreateCompatibleBitmap(srcdc,roi[2], roi[3])
memdc.SelectObject(bmp)
memdc.BitBlt((0,0), (roi[2], roi[3]), srcdc, (roi[0], roi[1]), con.SRCCOPY)
signedInts = bmp.GetBitmapBits(True)
# cv2 magic
img = np.fromstring(signedInts, dtype='uint8')
img.shape = (roi[3], roi[2], 4)
srcdc.DeleteDC()
memdc.DeleteDC()
api.ReleaseDC(hwnd, wdc)
api.DeleteObject(bmp.GetHandle())



cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
print(img.shape)
cv2.imwrite('img.png', img)
