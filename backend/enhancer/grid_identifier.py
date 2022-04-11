import logging
import pyautogui as ui

import cv2

import utils.cv2_utils as utils

from enhancer.cell import Cell
from processes.recognizer import Recognizer
from jobs.helpers.extruder import Extruder

X_SHIFT = 1 # X_SHIFT and Y_SHIFT used to calibrate actual inventory grid position of found inventory feature
Y_SHIFT = 1
ITEM_WIDTH = 33
ITEM_HEIGHT = 33
MARGIN = 1
SIZE = [9, 11]
GRID_ENTRY = 'assets/enhancer/grid_identifier.png'
# GRID_ENTRY_2 = 'assets/enhancer/inventory_shop_active.png'
# todo change debug to image log, decorate it
# include size into class
# add option use image instead path
class GridIdentifier:

    def __init__(self, source, debug=False):
        self.debug = debug
        self.source = source
        self.log = logging.getLogger('grid-identifier')
        self.identifier = cv2.imread(GRID_ENTRY)
        # utils.show_image(self.identifier)
        self.col, self.row = SIZE
        self.entry = self._find_grid_entry()
        # print(self.entry)
        # utils.show_image(utils.circle(self.source, (*self.entry, 2), thickness=3))
        self.inventory_region = self._inventory_region()
        self.log.debug('Inventory region {0}'.format(self.inventory_region))
        # utils.show_image(utils.rect(self.source, self.inventory_region))

        self.cells = self.generate_rectangles(self.entry)


    def generate_rectangles(self, start):
        self.log.debug('Try generate rectangles: {0}, {1}'.format(self.col, self.row))
        x, y = start
        cells = []
        count = 0
        for row in range(self.row):
            for col in range(self.col):
                dx = x + (ITEM_WIDTH + MARGIN) * col + col
                dy = y + 1 + (ITEM_HEIGHT + MARGIN + 1) * row + row
                source = self.source[dy:dy+ITEM_HEIGHT, dx:dx+ITEM_WIDTH]
                config = {
                    "col": col,
                    "row": row,
                    "x": dx,
                    "y": dy,
                    "source": source,
                    "id": count
                }
                count+=1
                cells.append(Cell(**config))
        # import pdb; pdb.set_trace()
        self.log.debug('Cells generated')

        return cells

    def _find_grid_entry(self):
        self.log.debug('Grid anchor: {0}'.format(self.identifier.shape))
        grid_entry = Extruder(self.source).match_by_template(self.identifier, method='minmax')
        x, y, _, h = grid_entry
        self.log.debug('Found grid entry at: {0}'.format(grid_entry))
        return x + X_SHIFT, y + h + Y_SHIFT

    def _inventory_region(self):
        self.log.debug('Find inventory region')
        region = [self.entry[0] - 1, self.entry[1] - 1, self.col * (ITEM_WIDTH + 1) + self.col + 1,
                  self.row * (ITEM_HEIGHT + 1) + self.row + 1]
        return region
    
    def cells_image(self):
        for c in self.cells:
            self.source = utils.rect(self.source, c.rect())
            # self.source = utils.text(self.source, c.id, x=c.x, y=c.y)
        return self.source
        # utils.show_image(self.source)