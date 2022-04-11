import logging
import math

from enhancer.tasks.operator import Operator
from processes.click import Click
from processes.wait import Wait

class Destructor(Operator):

    def __init__(self, config, inventory):
        super().__init__(config, inventory)
        self.log = logging.getLogger('enhancer')
        self.destruct_button = self.config['assets']['destructor']['button_of_start']
        self.dx, self.dy = self.destruct_button
        self.dx, self.dy = int(self.dx), int(self.dy)
        self.select_delay = 0.1
        # import pdb; pdb.set_trace()

    def proceed(self):
        self.destroy()
        self.log.info('End destruction')
    
    def destroy(self):
        # for container in self.split_in_buckets():
        for _ in range(1):
            self.log.info('Destructor items {0}'.format(len(self.inventory.working_cells)))
            for cell in self.inventory.working_cells[:20]:
                x, y = self.finder.point(cell.center())
                Click(x,y, 'double').make_click()
                Wait(self.select_delay).delay()
            
            x, y = self._get_destruct_point()
            Click(180, 488, 'double').make_click()
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
    
    def _get_destruct_point(self):
        entry = self.inventory.grid.entry
        x,y = self.finder.point(entry)
        return self.dx + x, self.dy + y