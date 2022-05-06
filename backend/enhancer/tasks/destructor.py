import logging
import math

from enhancer.tasks.operator import Operator
from processes.click import Click
from processes.wait import Wait
from driver import click, double

class Destructor(Operator):

    def __init__(self, config, inventory):
        super().__init__(config, inventory)
        self.log = logging.getLogger('enhancer')
        self.destruct_button = self.config['assets']['destructor']['button_of_start']
        self.dx, self.dy = self.destruct_button
        self.dx, self.dy = int(self.dx), int(self.dy)
        self.select_delay = 0.1
        self.handle = self.inventory.handle

        # import pdb; pdb.set_trace()

    def proceed(self):
        self.destroy()
        self.log.info('End destruction')
    
    def destroy(self):
        rounds = len(self.split_in_buckets())
        # rounds = 2
        # for i, container in enumerate(range(rounds)):
        while True:
            # print('Destroying {0}/{1}'.format(i, rounds))
            # self.log.info('Destructor items {0}'.format(len(self.inventory.working_cells)))
            for cell in self.inventory.working_cells[:20]:
                x, y = self.finder.point(cell.center())
                y = y - 25
                double(x,y, self.handle)
                Wait(self.select_delay).delay()
            
            x, y = self._get_destruct_point()
            click(x,y, self.handle)
            Wait(3).delay()

            # self.update_inventory()
        self.log.info('Destructor rest items {0}'.format(len(self.inventory.working_cells)))
        
    def split_in_buckets(self):
        buckets = math.ceil(len(self.inventory.working_cells) / 20)
        containers = []
        step = 0
        for b in range(buckets):
            containers.append(self.inventory.working_cells[step:step+20])
            step += 20
        return containers

    def update_inventory(self):
        self.inventory.open_source()
        self.inventory.update_grid()
        self.inventory.set_params()
    
    def  _get_destruct_point(self):
        entry = self.inventory.grid.entry
        x,y = self.finder.point(entry)
        return self.dx + x, self.dy + y - 25