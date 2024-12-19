import threading
import multiprocessing
import config

from utils.deep_utils import get_active_windows
from ocr import get_char_name
from screen_reader import get_window_image
from farm_with_numbers import farming, necro, wind
from enhancer.invetory_dispatcher import InventoryDispatcher
from open_cards_job import open, plain
from taming import taming

CONFIG_FILE = 'config.yml'
STATE_FILE = 'state.yml'
CFG = config.load_config(CONFIG_FILE)
CHAR_CFG = config.load_config(STATE_FILE)

print('Create launchere')

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

def _ether(*args):
    cfg = args[0]
    inventory = InventoryDispatcher('enhancer.config.yml', cfg)
    return inventory.search()

def _farm(*args):
    return farming(args[0])

def _steel(*args):
    cfg = args[0]
    inventory = InventoryDispatcher('enhancer.config.yml', cfg)

operations = {
    'enchant': _enchant,
    'destroy': _destroy,
    'farm': _farm,
    'necro': necro,
    'cards': open,
    'taming': taming,
    'awake': _awake,
    'combine': _combinate,
    'plain': plain,
    'wind': wind,
    'ether': _ether,
    'steel': _steel
}

def run(handle, char_name):
    char_name = get_char_name(get_window_image(handle))
    th = None

    roles = CHAR_CFG['roles']

    if char_name not in roles:
        return
    role = roles[char_name]
    cfg = role
    cfg['handle'] = handle
    cfg['name'] = char_name

    operations[role['type']](cfg)

def stop(process):
    print(process)
    process.terminate()
    return True

def clients_state():
    handles = get_active_windows(CFG['whandle'])
    state = dict()
    for handle in handles:
        if handle == 0:
           continue
        # import cv2
        # cv2.imshow('Image', get_window_image(handle))
        # cv2.waitKey(0)
        
        char_name = get_char_name(get_window_image(handle))
        roles = CHAR_CFG['roles']
        if char_name not in roles:
            continue
        role = roles[char_name]
        role['char_name'] = char_name
        state[handle] = role
        print(state)
    return state

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

            if role['type'] == 'steel':
                t1 = threading.Thread(target=operations['farm'], args=(cfg,))
                t1.daemon = True
                t1.start()
                t2 = threading.Thread(target=operations['destroy'], args=(cfg,))
                t2.daemon = True
                t2.start()
                continue
            th = threading.Thread(target=operations[role['type']], args=(cfg,))

        if th:
            th.daemon = True
            th.start()

def shutdown(th):
    th.stop()