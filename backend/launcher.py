import threading
import multiprocessing
import config

from farm_with_numbers import start
from utils.deep_utils import get_active_windows
from ocr import get_char_name
from screen_reader import get_window_image
from farm_with_numbers import farming, stop

CONFIG_FILE = 'config.yml'
STATE_FILE = 'state.yml'
CFG = config.load_config(CONFIG_FILE)
FARMERS = config.load_config(STATE_FILE)
state = dict()

def threads():
    handles = get_active_windows(CFG['whandle'])

    for handle in handles:
        if handle == 0:
           continue
        char_name = get_char_name(get_window_image(handle))
        if char_name in FARMERS['farmers']:
            # print('PID, Char: ', str(hwnd), char_name)
            print('handle:', str(handle), type(handle))
            state[handle] = dict()
            state[handle]['char'] = char_name
            state[handle]['alive'] = True
            state[handle]['handle'] = handle
            th = threading.Thread(target=farming, args=(handle,))
            th.daemon = True
            state[handle]['process'] = th
        if th:
            th.start()
            # th.join()