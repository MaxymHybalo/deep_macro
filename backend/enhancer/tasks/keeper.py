from enhancer.tasks.operator import Operator
from enhancer.inventory import Inventory

from processes.wait import Wait
from driver import double, click, move, drag, press, alt
from jobs.helpers.extruder import Extruder

ALL_POSITION = (700, 445)
OK_POSITION = (650, 445)
COUNTER_WINDOW = 'assets/counter_identifier.png'

class Keeper(Operator):
    def __init__(self, config, inventory):
        super().__init__(config, inventory)
        self.inventory = inventory
        self.handle = self.inventory.handle
        print('CFG', config)
        self.loops = config['config']['cycles']

    def proceed(self):
        print('ETHER HANDLER')
        self.stage()

    def stage(self):
        press(self.handle, '0')
        Wait(0.2).delay()
        self.refresh()
        while(len(self.inventory.working_cells) > 0):
            for (i, cell) in enumerate(self.inventory.working_cells):
                x, y = self.finder.point(self.inventory.working_cells[0].center())
                double(x, y - 25, self.handle)

                Wait(0.1).delay()
                ax, ay = ALL_POSITION
                click(ax, ay - 25, self.handle)
                Wait(0.1).delay()
                
                cx, cy = OK_POSITION
                click(cx, cy - 25, self.handle)
                Wait(0.1).delay()
            self.refresh()
        press(self.handle, 'i')
        Wait(0.4).delay()
        press(self.handle, 'i')


    def refresh(self):
        self.inventory.open_source()
        self.inventory.update_grid()
        self.inventory.set_params()
        print('cells 1', len(self.inventory.working_cells))
        
