from enhancer.helpers import Finder
from enhancer.cell import Cell
from processes.click import Click
from shapes.rect import Rect
from driver import click, double
from time import sleep
class Operator:
    def __init__(self, config, inventory):
        super().__init__()
        self.config = config
        self.inventory = inventory
        self.finder = Finder()
    
    def click_at(self, key, method='click'):
        target = getattr(self.inventory, key)
        x,y = 0, 0
        if target is None:
            return
        if type(target) is Cell:
            x,y = target.center()
        else:
            x, y = Rect(target).center()
        x,y = self.finder.point((x,y - 25))
        # print('point', key, x,y, 'target', target)
        if method == 'double':
            # print('self.inventory.handle', self.inventory.handle)
            double(x,y, self.inventory.handle)
        else:
            click(x,y, self.inventory.handle)


