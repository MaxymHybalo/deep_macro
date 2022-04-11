import logging
from processes.click import Click
from processes.wait import Wait
from enhancer.tasks.operator import Operator

class Unpacker(Operator):

    def __init__(self, config, inventory):
        super().__init__(config, inventory)
        self.log = logging.getLogger('unpacker')
        self.log.info('Unpacker init')
        self.delay = 1.5

    def proceed(self):
        self.log.info('Unpacking')
        self.unpack()
        self.log.info('End unpacking')


    def unpack(self):
        for cell in self.inventory.working_cells:
            x, y = self.finder.point(cell.center())
            Click(x,y, 'double').make_click()
            Wait(0.4).delay()
            self.click_at('make')
            Wait(self.delay).delay()
            self.click_at('main_slot', 'double')