import logging

import cv2

from enhancer.cell import Cell
from enhancer.grid_identifier import GridIdentifier, ITEM_HEIGHT, ITEM_WIDTH
from enhancer.helpers import Finder
from jobs.helpers.detector import Detector
from processes.recognizer import Recognizer
import utils.cv2_utils as utils # used for drawing images


FILE = 'assets/enhancer/inventory.png'
class Inventory:

    def __init__(self, config, cfg):
        self.log = logging.getLogger('enhancer-v2')
        self.log.info('Created new enhancer instance')
        self.log.info('Config, {0}'.format(config))
        self.config = config
        self.config['enhancement']['cube'] = cfg['cube'] if 'cube' in cfg else self.config['enhancement']['cube']
        self.handle = cfg['handle']
        self.fnd = Finder()
        self.open_source()
        self.update_grid()
        self.set_params()

    def open_source(self):
        # self.source = cv2.imread(FILE)
        self.source = self._source()
        self.log.info('Loaded source screen')
        # utils.show_image(self.source)

    def set_params(self):
        self.cube = self.config['enhancement']['cube']
        cube_col, cube_row = self.cube
        self.cube_id = self.fnd.by_id(int(cube_col) - 1, int(cube_row) - 1)
        self.cube = self.grid.cells[self.cube_id]
        self.empty_item = cv2.imread('assets/' + self.config['recognize']['grid']['eoi'] + '.png')
        self.eoi = self.find_first_entry(self.empty_item)
        self.make = cv2.imread('assets/' + self.config['recognize']['enhance']['make'] + '.png')
        self.make = Detector(self.handle).find(self.make, self.source)
        # print('self.make', self.make)
        _ms_x, _ms_y, _, _ = self.make if self.make else (0,0,0,0)
        self.main_slot = _ms_x - 230, _ms_y - 55, 10, 10

        # print('self.cube_id', self.cube_id)
        # print('self.cube', self.cube)
        # print('self.eoi', self.eoi)
        # print('self.main_slot', self.main_slot)
        # print('self.make', self.make)
        # print('self.main_slot', self.main_slot)

        end_id = self.grid.cells[-1].id
        if self.eoi:
            end_id = self.eoi.id
        self.working_cells = self.grid.cells[self.cube.id + 1:end_id]


    def find_first_entry(self, target):
        entry = None
        for cell in self.grid.cells:
            empty = Detector(self.handle).find(self.empty_item, cell.source)

            if empty:
                if entry:
                    if cell.row < entry.row or (cell.col < entry.col and cell.row <= entry.row):
                        entry = cell
                else:
                    entry = cell
        return entry

    def _log_inventory(self, dictionary):
        # import pdb; pdb.set_trace()
        for key, value in dictionary.items():
            self.log.debug('{0}: {1}'.format(key, value))
    
    def update_grid(self):
        self.grid =  GridIdentifier(self.source)

    def _source(self):
        from screen_reader import get_window_image
        return get_window_image(self.handle)
        # from shapes.window import Window
        # import numpy
        # return numpy.array(Window(self.handle).update_window())
