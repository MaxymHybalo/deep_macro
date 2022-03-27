from win32 import win32gui as api

def get_window_coord(whandle):
	rect = api.GetWindowRect(whandle)
	l,t,r,b = rect
	w = r - l
	h = b - t
	return l, t, w, h