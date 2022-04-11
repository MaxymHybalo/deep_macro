from enhancer.helpers import Finder
from enhancer.cell import Cell
from processes.click import Click
from shapes.rect import Rect

class Operator:
    def __init__(self, config, inventory):
        super().__init__()
        self.config = config
        self.inventory = inventory
        self.finder = Finder()
    
    def click_at(self, key,  method='click'):
        target = getattr(self.inventory, key)
        x,y = 0, 0
        print('target', target)
        if target is None:
            return
        if type(target) is Cell:
            x,y = target.center()
        else:
            x, y = Rect(target).center()
        x,y = self.finder.point((x,y))
        Click(x,y, method).make_click()
