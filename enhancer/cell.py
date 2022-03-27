import logging

# import utils.cv2_utils as utils # used for drawing images
ITEM_WIDTH = 33
ITEM_HEIGHT = 33
class Cell:
    def __init__(self, **kwargs):
        self.log = logging.getLogger('cell')

        for key, value in kwargs.items():
            setattr(self, key, value)
            # self.log.info('Cell prop {0} is: {1}'.format(key, getattr(self, key)))
    
    def rect(self):
        self.log.warn('Cell rect')
        return self.x, self.y, ITEM_WIDTH + 1, ITEM_WIDTH + 1
    
    def center(self):
        return self.x + int(ITEM_WIDTH / 2), self.y + int(ITEM_HEIGHT / 2)