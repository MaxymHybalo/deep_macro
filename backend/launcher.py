import threading
import multiprocessing
import config

from farm_with_numbers import start
from utils.deep_utils import get_active_windows
from ocr import get_char_name
from screen_reader import get_window_image
from farm_with_numbers import farming, necro
from enhancer.invetory_dispatcher import InventoryDispatcher

CONFIG_FILE = 'config.yml'
STATE_FILE = 'state.yml'
CFG = config.load_config(CONFIG_FILE)
CHAR_CFG = config.load_config(STATE_FILE)
state = dict()

def _enchant(*args):
    cfg = args[0]
    inventory = InventoryDispatcher('enhancer.config.yml', cfg)
    return inventory.enhance()

def _destroy(*args):
    cfg = args[0]
    print('_destroy', cfg)
    inventory = InventoryDispatcher('enhancer.config.yml', cfg)
    return inventory.destroy()

operations = {
    'enchant': _enchant,
    'destroy': _destroy,
    'farm': farming,
    'necro': necro
}

def threads():
    handles = get_active_windows(CFG['whandle'])

    for handle in handles:
        if handle == 0:
           continue
        char_name = get_char_name(get_window_image(handle))
        roles = CHAR_CFG['roles']
        th = None
        if char_name not in roles:
            continue
        role = roles[char_name]
        print('role', role)
        if role:
            cfg = role
            cfg['handle'] = handle
            print('start from ', operations[role['type']])
            th = threading.Thread(target=operations[role['type']], args=(cfg,))


        # if char_name in FARMERS['farmers']:
        #     # print('PID, Char: ', str(hwnd), char_name)
        #     print('handle:', str(handle), type(handle))
        #     state[handle] = dict()
        #     state[handle]['char'] = char_name
        #     state[handle]['alive'] = True
        #     state[handle]['handle'] = handle
        #     is_pets = char_name == 'Artifactory' or char_name == 'Harmony'
        #     th = threading.Thread(target=necro if is_pets else farming, args=(handle,))
        #     print(th)
        #     state[handle]['process'] = th

        # else:
        # #     pass
        #     # from open_cards_job import open
        #     # from taming import taming
        #     if char_name == 'Acedia' or char_name == 'nvidia':
        #         from enhancer.invetory_dispatcher import InventoryDispatcher
        #         inventory = InventoryDispatcher('enhancer.config.yml', handle)
        #         th = threading.Thread(target=inventory.enhance, args=(handle,))
        #     # th = threading.Thread(target=open, args=(handle,))
        #     # th = threading.Thread(target=taming, args=(handle,))

        if th:
            th.daemon = True
            th.start()

def shutdown():
    for th in state:
        state[th]['process'].stop()