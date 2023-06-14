from datetime import datetime
import cv2

from enhancer.tasks.operator import Operator
from enhancer.helpers import Finder

from driver import double, click, move, drag
from processes.wait import Wait
from jobs.helpers.extruder import Extruder
from ocr import crop_roi

# from ocr import crop_roi, get_awaking
# from utils.awaking_aggregator import normalize, compare
# from utils.reporter import buildFileName, report, initialize

ETHER_INPUT = 'assets/ether_input.png'
class Searcher(Operator):
    def __init__(self, config, inventory):
        super().__init__(config, inventory)
        self.inventory = inventory
        self.handle = self.inventory.handle

    def proceed(self):
        print('ETHER HANDLER')
        self.stage()

    def stage(self):
        cx, cy = self.inventory.cube.x, self.inventory.cube.y
        print('win' ,cx, cy)
        cy = cy - 25 - 55
        cx = cx + 60
        # drag(cx ,cy, cx + 10, cy + 20, self.handle)
        # drag(742, 169 - 25, 742 + 10, 169 - 25, self.handle)
        Wait(0.3).delay()
        for (i, cell) in enumerate(self.inventory.working_cells):
            x, y = self.finder.point(cell.center())
            # print('x, y:',i, x, y);
            click(x - 5, y - 25 - 5, self.handle)
            Wait(0.4).delay()
            move(x + 5, y - 25 + 5, 0, self.handle)
            Wait(0.5).delay()
            img = self.inventory._source()
            e = Extruder(img)
            res = e.match_by_template(cv2.imread(ETHER_INPUT), method='threshold')

            print(res)
            rx, ry, _, _ = res
            img = crop_roi(img, (rx, ry + 18, 135, 52))
            cv2.imwrite('logs/searching/{0}'.format(f'ring_{i}.png'), img)

            # click(x + 12,y - 25 + 5, self.handle)

