import cv2
from win32 import win32gui as api

def get_window_coord(whandle):
    rect = api.GetWindowRect(whandle)
    l,t,r,b = rect
    w = r - l
    h = b - t
    return l, t, w, h


def draw_grid(whandle, image=None):
    from screen_reader import get_window_image
    img = image if image is not None else get_window_image(whandle)
    _, _, w, h = get_window_coord(whandle)
    color = (19, 233, 50)
    thickness = 1
    delta = 5
    w_range = int(w / delta)
    for x in range(w_range + 1):
        dx = x * delta
        cv2.line(img, (dx, 0), (dx, h), color, thickness)
    
    for y in range(int(h / delta) + 1):
        dy = y * delta
        cv2.line(img, (0, dy), (w, dy), color, thickness)
    
    return img
    # cv2.imshow('test', img)
    # cv2.waitKey(0)

def get_active_windows(handle):
    process_whandles = []
    
    def handleWindow(hwnd, ctx):
        if api.GetWindowText(hwnd) == handle:
            process_whandles.append(hwnd)
            
    api.EnumWindows(handleWindow, None)
    print(process_whandles)
    return process_whandles


def _drop_rect(img, start, end):
    if img is not None:
        cv2.rectangle(img, start, end, (100,100,0), 5)
    cv2.imshow('Test', img)
    cv2.waitKey(0)