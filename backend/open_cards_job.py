import time
from driver import click
from win32 import win32gui as w


P1 = (690, 309 - 28)
P2 = (734, 245 - 28)
PLAIN_PONT = (729, 247 - 28)

DELAY = 2

def open(cfg):
    wnd = cfg['handle']
    while True:
        rect = w.GetWindowRect(wnd)
        print('rect', rect)
        l,t, r,b = rect
        x1, y1 = P1
        # x1 += l
        # y1 += t

        click(x1, y1, wnd)

        time.sleep(DELAY)

        x2, y2 = P2
        # x2 += l
        # y2 += t
        
        click(x2, y2, wnd)
        time.sleep(1)

def plain(cfg):
    wnd = cfg['handle']
    rect = w.GetWindowRect(wnd)

    while 708:
            l,t, r,b = rect
            x1, y1 = PLAIN_PONT
            # x1 += l
            # y1 += t

            click(x1, y1, wnd)

            time.sleep(0.5)
