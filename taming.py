import time
from driver import click, press, slide
from main import get_active_windows, CFG

CALL_TIMEOUT = 1
TAMING = 4
KILL = 2

# whandles = get_active_windows(CFG['whandle'])

# whandle = whandles[0]

def taming(whandle):
	while True:
	    press(whandle, '2')
	    time.sleep(CALL_TIMEOUT)
	    press(whandle, '3')
	    time.sleep(TAMING)
	    press(whandle, '1')
	    time.sleep(KILL)