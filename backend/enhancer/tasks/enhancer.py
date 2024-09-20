import logging
import utils.cv2_utils as utils
from processes.click import Click
from processes.wait import Wait
from shapes.rect import Rect
from enhancer.helpers import Finder
from enhancer.cell import Cell
from enhancer.tasks.operator import Operator
from driver import click, double

class Enhancer(Operator):

    def __init__(self, config, inventory):
        super().__init__(config, inventory)
        self.log = logging.getLogger('enhancer')
        self.log.info('Items to process: {0}'.format(len(self.inventory.working_cells)))
        self.delay = self.config['options']['await']
        self.handle = self.inventory.handle
        # self.show_state()

    def proceed(self):
        loops = int(self.config['options']['cycles'])
        print('Starting loops for handle: {0} cycles {1}'.format(self.handle, loops))
        self.log.info('Enhancing rounds: {0}'.format(loops))
        for l in range(loops):
            self.stage(l)

    def stage(self, cycle):
        self.setup(cycle)
        self.enhancing()
        self.clear()

    def enhancing(self):
        for (i, cell) in enumerate(self.inventory.working_cells):
            x, y = self.finder.point(cell.center())
            y = y - 25
            # Click(x,y, 'double', handle).make_click()
            double(x,y, self.handle)

            # Dust enchant
            # Wait(0.3).delay()
            # x1, y1 = self.finder.point(self.inventory.working_cells[0].center())
            # y1 = y1 - 25
            # double(x1, y1, self.handle)
            # Wait(0.3).delay()
            # End Dust enchant
            self.click_at('cube', 'double')
            if self.config['mode'] == 'binary':
                second_item = self.inventory.working_cells[i+1]
                x2, y2 = self.finder.point(second_item.center())
                y2 = y2 - 25
                double(x2, y2, self.handle)
            Wait(0.4).delay()
            self.click_at('make')
            Wait(self.delay).delay()
            self.click_at('main_slot', 'double')


    def setup(self, cycle):
        self.current_cycle = cycle
        self.click_at('main_slot', 'double')
        self.log.info('Setup round {0}'.format(self.current_cycle))

    def clear(self):
        self.click_at('main_slot', 'double')
        self.click_at('eoi', 'double')
        self.log.info('Ended round {0}'.format(self.current_cycle))
    
    def main_click(self):
        Rect(self.finder.point(self.main)).click().make_click()


    def show_state(self):
        img = self.inventory.grid.cells_image()
        img = utils.rect(img, self.inventory.cube.rect(), 3, 3)
        # for c in self.inventory.working_cells:
        #     img = utils.rect(img, c.rect(), (199,200,0), 3)
        # img = utils.rect(img, self.inventory.eoi.rect(), (30,100, 20), 3)
        print(self.inventory.main_slot)
        img = utils.rect(img, self.inventory.main_slot, (0, 200, 0),1)
        img = utils.rect(img, self.inventory.make, (100, 200, 0), 2)
        utils.show_image(img)