import time
from datetime import datetime
import cv2

from enhancer.tasks.operator import Operator
from enhancer.helpers import Finder

from driver import double, click, move, drag, press
from processes.wait import Wait
from jobs.helpers.extruder import Extruder
from ocr import crop_roi, get_text
from utils.ether_aggregator import capture, is_back_caption

from shapes.rect import Rect
# from ocr import crop_roi, get_awaking
# from utils.awaking_aggregator import normalize, compare
# from utils.reporter import buildFileName, report, initialize

ETHER_INPUT = 'assets/ether_input.png'
ETHER_ROI_WIDTH = 145
DESTROY = 'assets/enhancer/disassamble_2.png'
LOCKED_RING_1 = 'assets/khoradrick.png'
LOCKED_RING_2 = 'assets/mortis.png'
KEEPER_ID = 'assets/keeper_id.png'
KEEPER_KEY = '0'

RING_TYPES_COORDS = {
    'first': (730, 498),
    'second': (730, 520)
}


class Searcher(Operator):
    def __init__(self, config, inventory):
        super().__init__(config, inventory)
        self.inventory = inventory
        self.handle = self.inventory.handle

    def proceed(self):
        print('ETHER HANDLER')
        self.stage()

    def stage(self):
        s = time.time()
        staging = True
        while staging:
            # self.shake_window()
            Wait(0.3).delay()
            for (i, cell) in enumerate(self.inventory.working_cells[0:18]):
                x, y = self.finder.point(cell.center())
                # print('x, y:',i, x, y);
                move(x, y - 25, 0, self.handle)
                click(x - 5, y - 25 - 5, self.handle)
                Wait(0.5).delay()
                move(x + 5, y - 25 + 5, 0, self.handle)
                Wait(0.5).delay()
                img = self.inventory._source()
                e = Extruder(img)
                res = e.match_by_template(cv2.imread(ETHER_INPUT), method='threshold')
                has_locked = self.check_locked_rings(img)
                if has_locked:
                    print('Locked Ring Found')
                    self.unlock_rings(has_locked)
                if not res:
                    continue
                print(res)
                rx, ry, _, _ = res
                img = crop_roi(img, (rx, ry + 18, ETHER_ROI_WIDTH, 52))
                match = capture(img)
                if not match:
                    double(x, y - 25, self.handle)
                else:
                    self.move_to_keeper(x, y)
                    break # move to start 
                Wait(0.3).delay()
            self.disassamble()
            self.shake_window()
            # click(x + 12,y - 25 + 5, self.handle)
        print(time.time() - s)

    def move_to_keeper(self, x, y):
        Wait(0.3).delay()
        press(self.handle, KEEPER_KEY)
        Wait(0.3).delay()

        img = self.inventory._source()
        e = Extruder(img)
        has_keeper = e.match_by_template(cv2.imread(KEEPER_ID), method='threshold')
        # cv2.rectangle(img, has_keeper, (255, 100, 50), 2)
        # cv2.imshow('Image', img)
        # cv2.waitKey(0)
        
        print('[Proceed keeper]: ', has_keeper)
        if has_keeper:
            double(x, y - 25, self.handle)
            Wait(0.4).delay()
            # kx, ky, w, _ = has_keeper
            # click(kx + w - 5, ky + 5 - 25, self.handle)
            Wait(0.4).delay()
            press(self.handle, 'i') # open destroy dialog
            Wait(0.2).delay()
            press(self.handle, 'l') # open destroy dialog
            Wait(0.4).delay()
            press(self.handle, 'i') # open destroy dialog
            Wait(0.4).delay()

    def check_locked_rings(self, img):
        e = Extruder(img)
        r1 = e.match_by_template(cv2.imread(LOCKED_RING_1), method='threshold')
        r2 = e.match_by_template(cv2.imread(LOCKED_RING_2), method='threshold')
        if r1:
            return 'first'
        elif r2:
            return 'second'
        else:
            return None

    def unlock_rings(self, type):
        click(250, 100 - 25, self.handle) # Free NPC area
        Wait(0.2).delay()
        click(730, 268 - 25, self.handle) # Select ring type
        Wait(0.2).delay()
        x, y = RING_TYPES_COORDS[type]
        click(x, y - 25, self.handle) # Select ring type
        Wait(2).delay()
        click(730, 330 - 25, self.handle) # Enchant
        Wait(1).delay()
        x, y = self.inventory.grid.entry
        y = y - 25 - 30

        img = self.inventory._source()
        print('Has back button: ', is_back_caption(img))
        if is_back_caption(img):
            click(730, 245 - 25, self.handle) # Return back
            Wait(0.2).delay()
            click(x, y , self.handle) # Select enchant window
        else:
            while not is_back_caption(img):
                Wait(1).delay()
                print('Open rings next tick', is_back_caption(img))
                click(730, 245 - 25, self.handle) # Repeat
                Wait(1).delay()
                img = self.inventory._source()
                # cv2.imshow('Image', img)
                # cv2.waitKey(0)
                
            click(730, 245 - 25, self.handle) # Return back
            Wait(0.2).delay()
            click(x, y , self.handle) # Select enchant window

    def disassamble(self):
        source = self.inventory._source()
        e = Extruder(source)
        res = e.match_by_template(cv2.imread(DESTROY), method='threshold')
        print('res', res)
        if not res:
            return
        x, y = Rect(res).center()
        print('destroy', x, y)
        click(x, y - 25, self.handle)
        Wait(4.3).delay()

    def shake_window(self):
        # print(self.inventory.grid.entry)
        x, y = self.inventory.grid.entry
        y = y - 25 - 30

        # Wait(0.3) 
        # drag(x, y, x - 10, y + 20, self.handle)
        # Wait(0.2).delay()
        # drag(x - 10, y + 20, x + 10, y - 20, self.handle)
        press(self.handle, 'i')
        Wait(0.2).delay()
        press(self.handle, 'i')
        Wait(0.2).delay()
        press(self.handle, 'l')
        Wait(0.2).delay()

        # fx, fy = self.inventory.working_cells[0].center()
        
        # click(fx, fy - 25, self.handle)
        # Wait(0.5)
        # click(fx, fy - 25, self.handle)

        # click(fx, fy - 25, self.handle)
        # Wait(0.2).delay()

