import time
from datetime import datetime
import cv2

from enhancer.tasks.operator import Operator
from enhancer.helpers import Finder

from driver import double, click, move, drag, press
from processes.wait import Wait
from jobs.helpers.extruder import Extruder
from ocr import crop_roi
from utils.ether_aggregator import capture

from shapes.rect import Rect
# from ocr import crop_roi, get_awaking
# from utils.awaking_aggregator import normalize, compare
# from utils.reporter import buildFileName, report, initialize

ETHER_INPUT = 'assets/ether_input.png'
ETHER_ROI_WIDTH = 145
DESTROY = 'assets/enhancer/disassamble_2.png'

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

        for j in range(int(100 / 20)):
            # self.shake_window()
            Wait(0.3).delay()
            print(len(self.inventory.working_cells[0:20]))
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
                if not res:
                    continue
                print(res)
                rx, ry, _, _ = res
                img = crop_roi(img, (rx, ry + 18, ETHER_ROI_WIDTH, 52))
                match = capture(img)
                if not match:
                    double(x, y - 25, self.handle)
                Wait(0.3).delay()
                cv2.imwrite('logs/searching/{0}'.format(f'ring_{i}.png'), img)
            self.disassamble()
            self.shake_window()
            # click(x + 12,y - 25 + 5, self.handle)
        print(time.time() - s)

    def disassamble(self):
        source = self.inventory._source()
        e = Extruder(source)
        res = e.match_by_template(cv2.imread(DESTROY), method='threshold')
        print('res', res)
        x, y = Rect(res).center()
        print('destroy', x, y)
        click(x, y - 25, self.handle)
        Wait(1.3).delay()

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

