import logging
from pydoc import cli
import utils.cv2_utils as utils
import pyautogui as ui
from processes.click import Click
from processes.wait import Wait
from shapes.rect import Rect
from enhancer.helpers import Finder
from enhancer.cell import Cell
from enhancer.tasks.operator import Operator
from driver import click, double, send

class Combinator(Operator):

    def __init__(self, config, inventory):
        super().__init__(config, inventory)
        self.log = logging.getLogger('enhancer')
        self.log.info('Items to process: {0}'.format(len(self.inventory.working_cells)))
        self.delay = self.config['options']['await']
        self.handle = self.inventory.handle
        self.cfg = self.config['config']
        self.loops = self.cfg['cycles']
        # self.show_state()

    def proceed(self):
        loops = self.loops
        print('Starting loops for handle: {0} cycles {1}'.format(self.handle, loops))
        self.log.info('Enhancing rounds: {0}'.format(loops))
        Wait(2).delay()
        for l in range(loops):
            self.stage(1)

    def stage(self, cycle):
        # self.setup(cycle)
        # self.enhancing()
        # self.clear()
        self._put_entity((1, 11))
        Wait(0.3).delay()
        ui.write('70', interval=0.01)
        ui.press('enter')
        Wait(0.3).delay()
        
        self._put_entity((2, 11))
        Wait(0.3).delay()

        ui.write('560', interval=0.01)
        ui.press('enter')
        Wait(0.4).delay()

        combintation = self._get_cell((1, 11))
        combintation = x, y = combintation.x - 40 , combintation.y + 30
        print(combintation)
        click(combintation[0], combintation[1], self.handle)

        Wait(1.1).delay()




    def _put_entity(self, entity):
        item_source = self._get_cell(entity)
        x, y = item_source.x, item_source.y
        double(x, y, self.handle)

    def _get_cell(self, entity):
        id = self.inventory.fnd.by_id(int(entity[0]) - 1, int(entity[1]) - 1)
        return self.inventory.grid.cells[id]


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