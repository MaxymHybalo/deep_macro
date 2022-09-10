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
from ocr import crop_roi, get_awaking
from utils.awaking_aggregator import normalize, compare
from utils.reporter import buildFileName, report, initialize

class Awakening(Operator):
    def __init__(self, config, inventory):
        super().__init__(config, inventory)
        self.inventory = inventory
        self.handle = self.inventory.handle
        self.item = config['config']['item']
        self.scroll = config['config']['scroll']
        self.stone = config['config']['stone']
        self.goals = config['config']['state']
        self.report_file = buildFileName(config['config']['name'])
        initialize('awaking', self.report_file)
        print('awake', self.scroll, self.stone, self.item)
        scroll_source = self._get_cell(self.scroll)
        print('cell', scroll_source.x,scroll_source.y)
        print('make', self.inventory.make)
        
    def proceed(self):
        processing = True
        counter = 0
        while processing:
            self.stoning()
            Wait(3).delay()
            captured = self.capturing(counter)

            if captured:
                print('captured!!!')
                processing = False
            else:
                counter = counter + 1

                self.click_at('main_slot', 'double')
                Wait(0.3).delay()

                self.scrolling()

                Wait(1.2).delay()

        print('FOUNDED')

    def capturing(self, counter):
        # awake +
        # get window +
        # get source +
        # extract data +
        # normalaize +-
        # save ~
        # compare data +
        # analyze
        log_name = 'awake_{}.png'.format(datetime.now().strftime('%H_%M_%S_%d_%m_%y'))
        roi_rect = (442, 388, 402, 80)
        window = self.inventory._source()
        img = crop_roi(window, roi_rect)
        cv2.imwrite('logs/awaking/{0}'.format(log_name), img)
        data = normalize(get_awaking(img))
        stats = compare(data, self.goals)
        report('awaking', self.report_file, (counter, data, stats, log_name))
        print('capture result', stats)

        if stats is None:
            return False
        return True
        # print(data)
        # print('stats', stats)
        # cv2.imshow('Image', img)
        # cv2.waitKey(0)
        


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
