import logging
import time
import datetime
import numpy as np
from processes.recognizer import Recognizer
from processes.wait import Wait
from utils.configurator import Configurator
from jobs.grid_layout import Grid
import utils.cv2_utils as utils
from utils.drawer import draw_state 
from shapes.rect import Rect

class Enhancer:

    def __init__(self, config):
        self.log = logging.getLogger('enhancer')
        self.config = config
        self.cube = None
        self.grid = None
        self.now = datetime.datetime.now()
        self.round = 0
        self.mode = self.config['mode']

    def process(self):
        cycles = int(self.config['enhancement']['cycles'])
        for i in range(cycles):
            self.round = i
            self.enhance()
        self.log.debug('End Enhancer process')


    def state(self):
        self.log.debug('Getting inventory state')
        grid_image = self.image_path(self.config['recognize']['grid']['image'])
        self.grid = Grid(grid_image)
        eoi = self.grid.find_position(self.image_path(self.config['recognize']['grid']['eoi']))
        self.cube = self.config['enhancement']['cube']
        self.cube = list(map(lambda x: int(x), self.cube))
        scope = self.grid.slice_inventory([self.cube[0] + 1, self.cube[1]], eoi)
        self.log.debug('Inventory state proceed')
        return scope, eoi

    def enhance(self):
        scope, _ = self.state()
        # self.click_at_target(self.config['recognize']['enhance']['menu'])
        if self.mode == 'disassamble':
            self._break(scope)
        elif self.mode == 'single':
            self.do_flow(scope)
        else:
            self.do_binary_flow(scope)

    def do_flow(self, scope):
        make, main, cube = self._init_flow()
        self.log.info('Start enhancing from {0}'.format(len(scope)))
        cube.make_click()
        cube.process = 'dclick'

        items = flatten(scope)
        for item in items:
            self.log.info('Item: {0}'.format(item))
            Rect(item).click().make_click()
            cube.make_click()
            make.make_click()
            main.make_click()
            # Wait(4).delay()

        cube.process = 'click'
        cube.make_click()
        main.make_click()


    def _break(self, scope):
        # make, main, cube = self._init_flow()
        print('[make]', self.config['recognize']['enhance'])

        make = self.click_at_target(self.config['recognize']['enhance']['disassamble'], make=False)
        self.log.info('Start enhancing from {0}'.format(len(scope)))
        # cube.make_click()
        # cube.process = 'dclick'
        slots = flatten(scope)
        size = len(slots)
        print('[scope]', scope)
        print('[slots]', slots)

        while len(slots) > 1:
            for i, s in enumerate(slots):
                if i == 19:
                    break
                item = Rect(s).click().make_click()
            # make
            make.make_click()

            
            if i < size - 1:
                item2 = Rect(slots[i+1]).click().make_click()
                self.log.info('Item 1 {0}, item 2 {1}'.format(s, slots[i+1]))

            # cube.make_click()
            # make.make_click()
            # main.make_click()
        
        # cube.process = 'click'
        # cube.make_click()
        # main.make_click()


    def do_binary_flow(self, scope):
        make, main, cube = self._init_flow()
        self.log.info('Start enhancing from {0}'.format(len(scope)))
        cube.make_click()
        cube.process = 'dclick'

        slots = flatten(scope)
        size = len(slots)

        for i, s in enumerate(slots):
            item = Rect(s).click().make_click()
            print('i < size', i, size)
            if i < size - 1:
                item2 = Rect(slots[i+1]).click().make_click()
                self.log.info('Item 1 {0}, item 2 {1}'.format(s, slots[i+1]))

            cube.make_click()
            make.make_click()
            main.make_click()
        
        cube.process = 'click'
        cube.make_click()
        main.make_click()

    def _init_flow(self):
        make = self.click_at_target(self.config['recognize']['enhance']['make'], make=False)
        make.delay = 1
        make.process = 'click'
        main = self.click_at_target(self.config['recognize']['enhance']['slot'], make=False)
        cube = Rect(self.grid.get_region_of(self.cube[0], self.cube[1])).click()
        cube.process = 'click'
        return make, main, cube

    def remove_broken(self, broken):
        remove_points = self.config['recognize']['remove']
        self.click_at_target(remove_points['menu'])
        self.select_broken(broken)
        self.click_at_target(remove_points['clear'])
        time.sleep(0.5)
        self.click_at_target(remove_points['confirm'])
        self.click_at_target(remove_points['close'])
        self.log.critical('Removed: {0}'.format(len(broken)))

    def select_broken(self, broken):
        for b in broken:
            Rect(b).click().make_click()

    def click_at_target(self, target, make=True):
        click = Recognizer(self.image_path(target), region=None)\
            .recognize(once=True)
        click = Rect(click).click()
        if make:
            click.make_click()
            self.log.debug('Click at {0}'.format(target))
        return click

    # TODO try get region of all inventory and then split to parts
    def fetch_scope_mask(self, scope):
        self.log.debug('Start fetching a images')
        result = list(map(lambda col: list(map(lambda cell: utils.make_image(region=cell), col)), scope))
        self.log.debug('End fetching a images')
        return result

    def image_path(self, image):
        path = self.config['recognize']['prefix']['path']
        prefix = self.config['recognize']['prefix']['image_suffix']
        full_path = path + image + prefix
        self.log.debug('Grid identifier: {0}'.format(full_path))
        return full_path

    def logged_image_name(self, moment):
        return 'log/' + moment + '_cycle_' + str(self.round) + '_' + str(self.now.year) + '_' + str(self.now.month) \
               + '_' + str(self.now.day) + '_' + str(self.now.hour) + '_' + str(self.now.minute) + '.png '

def flatten(source):
    result = []
    for s in source:
        result.extend(s)
    return result
