import logging
import pyautogui as ui
import time
import numpy as np
import cv2


class Recognizer:

    def __init__(self, image, region, wait=0, process="recognize", **kwargs):
        self.log = logging.getLogger('recognizer')
        self.image = image
        self.region = region
        self.wait = wait
        self.process = process
        self.properties = kwargs

    def recognize(self, once=False):
        self.log.debug('Try to recognize {0}'.format(self.image))
        value = ui.locateOnScreen(str(self.image), region=self.region)
        if once:
            self.log.debug('Recognized once: {0}'.format(value))
            return value
        while value is None:
            time.sleep(self.wait)
            value = ui.locateOnScreen(str(self.image), region=self.region)
        self.log.debug('Recognized: {0}'.format(value))
        return value

    def recognize_all(self):
        if self.region is not None:
            return ui.locateAllOnScreen(self.image, region=self.region)
        return ui.locateAllOnScreen(self.image,)

    def center_of(self):
        location = self.recognize()
        center = ui.center(location)
        return {
            'x': center[0],
            'y': center[1]
        }

    def __str__(self):
        return 'image: ' + self.image + ' region: ' + str(self.region)
