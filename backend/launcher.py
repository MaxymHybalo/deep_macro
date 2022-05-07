import threading
import multiprocessing
import config

from farm_with_numbers import start
from utils.deep_utils import get_active_windows
from ocr import get_char_name
from screen_reader import get_window_image
from farm_with_numbers import farming, necro
from enhancer.invetory_dispatcher import InventoryDispatcher
from open_cards_job import open
from taming import taming

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

def _combinate(*args):
    cfg = args[0]
    print('_destroy', cfg)
    inventory = InventoryDispatcher('enhancer.config.yml', cfg)
    return inventory.combinate()

def _awake(*args):
    cfg = args[0]
    inventory = InventoryDispatcher('enhancer.config.yml', cfg)
    return inventory.awake()
# def _steel(*args):
#     cfg = args[0]
#     inventory = InventoryDispatcher('enhancer.config.yml', cfg)

operations = {
    'enchant': _enchant,
    'destroy': _destroy,
    'farm': farming,
    'necro': necro,
    'cards': open,
    'taming': taming,
    'awake': _awake,
    'combine': _combinate
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
            cfg['name'] = char_name
            # print('start from ', operations[role['type']])
            if role['type'] == 'steel':
                t1 = multiprocessing.Process(target=operations['farm'], args=(cfg,))
                t1.daemon = True
                t1.start()
                t2 = multiprocessing.Process(target=operations['destroy'], args=(cfg,))
                t2.daemon = True
                t2.start()
                state[char_name] = (t1, t2)
                continue
            th = multiprocessing.Process(target=operations[role['type']], args=(cfg,))

        if th:
            th.daemon = True
            th.start()
            state[char_name] = (th)
    
    # print('Threads', state)
    return state

def shutdown():
    for key, thread in state.items():
        print('Terminating',  key, thread)
        thread.terminate()
        thread.join()