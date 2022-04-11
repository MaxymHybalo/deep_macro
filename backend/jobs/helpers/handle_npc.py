import cv2
from utils.cv2_utils import screenshot

from shapes.window import Window
from shapes.rect import Rect

from jobs.helpers.extruder import Extruder

from processes.click import Click
from processes.wait import Wait

DELAY = 0.3

class HandleNpc:

    def __init__(self):
        pass

    def select_menu(self, config, quality='minmax'):
        Wait(DELAY).delay()
        e = Extruder(screenshot(Window().rect))
        template = cv2.imread(config.path)
        menu = e.match_by_template(template, roi=config.roi, method=quality)
        if not menu:
            return None

        point = Rect(menu).center()
        x,y = Window().relative(point)
        Click(x,y).make_click()
        return x, y
