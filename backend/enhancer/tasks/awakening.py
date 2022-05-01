# Plan
# 1. awake item + 
# 2. read results +
# 3. compare results -
# 4. if acceptable results stop 
# 5. scroll item 
# 6. repeat 
from datetime import datetime
import cv2
from enhancer.tasks.operator import Operator
from enhancer.helpers import Finder

from driver import double, click
from processes.wait import Wait
from ocr import crop_roi

class Awakening(Operator):
    def __init__(self, config, inventory):
        super().__init__(config, inventory)
        self.inventory = inventory
        self.handle = self.inventory.handle
        self.item = config['config']['item']
        self.scroll = config['config']['scroll']
        self.stone = config['config']['stone']
        print('awake', self.scroll, self.stone, self.item)
        scroll_source = self._get_cell(self.scroll)
        print('cell', scroll_source.x,scroll_source.y)
        print('make', self.inventory.make)
        
        
    def proceed(self):
        self.stoning()
        Wait(3).delay()
        self.capturing()
        # self.scrolling()


        # self.click_at('main_slot', 'double')

    def capturing(self):
        # awake +
        # get window +
        # get source +
        # extract data +
        # normalaize - next step
        # save
        # compare date
        # analyze
        log_name = 'awaket_{}.png'.format(datetime.now().strftime('%H_%M_%S_$d_$m_$Y'))
        roi_rect = (442, 388, 402, 80)
        window = self.inventory._source()
        img = crop_roi(window, roi_rect)

        cv2.imwrite('logs/awaking/{0}'.format(log_name), img)
        cv2.imshow('Image', img)
        cv2.waitKey(0)
        


    def scrolling(self):
        self._put_entity(self.item)
        self._put_entity(self.scroll)
        # double(self.inventory.main_slot[0], self.inventory.main_slot[1], self.handle)
        Wait(0.4).delay()

        self.click_at('make')

    def stoning(self):
        self._put_entity(self.item)
        self._put_entity(self.stone)
        # double(self.inventory.main_slot[0], self.inventory.main_slot[1], self.handle)
        Wait(0.4).delay()

        self.click_at('make')


    def _put_entity(self, entity):
        item_source = self._get_cell(entity)
        x, y = item_source.x, item_source.y
        double(x, y, self.handle)

    def _get_cell(self, entity):
        id = self.inventory.fnd.by_id(int(entity[0]) - 1, int(entity[1]) - 1)
        return self.inventory.grid.cells[id]
