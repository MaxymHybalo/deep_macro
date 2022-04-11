import logging
import pyautogui as ui
import matplotlib.pyplot as plt
import numpy as np
from utils.configurator import Configurator
from utils.singleton import Singleton
from utils.deep_utils import get_window_coord
class Window(metaclass=Singleton):

    def __init__(self, handle):
        self.log = logging.getLogger('window')
        l, t, w, h = get_window_coord(handle)
        self.width, self.height = w, h
        self.x = l
        self.y = t
        self.rect = (self.x, self.y, self.width, self.height)

    def position(self):
        return self.x, self.y

    def locate_window(self):
        if not hasattr(self, 'windowHead'):
            self.windowHead = ui.locateOnScreen(self.config['marker'])
            self.log.info('Located game window on screen')
        else:
            print('window already inited: ', self.windowHead)

    def update_window(self):
        self.screen = ui.screenshot(region=(self.x,self.y, self.width, self.height))
        return self.screen
        
    def center(self):
        return self.x + int(self.width / 2), self.y + int(self.height / 2)

    def relative_center(self):
        return int(self.width / 2), int(self.height / 2)

    def relative(self, point):
        x, y = point
        return self.x + x, self.y + y