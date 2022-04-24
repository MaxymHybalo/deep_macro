import cv2
import numpy as np

from utils.cv2_utils import screenshot, draw_rect, show_image
from jobs.helpers.extruder import Extruder
from screen_reader import get_window_image
class Detector:

    def __init__(self, handle, observable=None, window=None):
        self.window = window
        self.handle = handle
        # import pdb; pdb.set_trace()
        self.observable = observable
        if type(observable) is str:
            self.observable = cv2.imread(observable)

    def detect(self):
        # move method head to once detection method if could be needed
        frame = get_window_image(self.handle)
        e = Extruder(frame)
        match = e.match_by_template(self.observable, method='threshold')
        while not match:
            image = get_window_image(self.handle)
            image = np.array(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            match = e.match_by_template(self.observable, image=image, method='threshold')
            frame = image
        return match

    def find(self, target, template):
        target = np.array(target)
        template = np.array(template)
        e = Extruder(target)
        match = e.match_by_template(target, image=template, method='threshold')
        return match
