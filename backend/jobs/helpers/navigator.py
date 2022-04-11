import logging

from processes.click import Click
from shapes.window import Window
from utils.cv2_utils import screenshot
from jobs.helpers.extruder import Extruder
from utils.config import Config
from processes.wait import Wait
from processes.move import Move
from shapes.rect import Rect

Y_OFFSET_FROM_START_POSITION = 70
TURN_AROUND_DISTANCE = 500

window = Window()
config = Config()
log = logging.getLogger('navigator')

class Navigator:

    @staticmethod
    def move_to_npc(npc_roi, npc=None):
        npc_x, npc_y = circus_npc_point(npc_roi)
        wx, wy = Window().position()
        Click(wx + npc_x + npc.nav_x_shift, wy + npc_y + npc.nav_y_shift, process='dclick').make_click()

    @staticmethod
    def click_at_npc(npc_roi, npc):
        npc_x, npc_y = circus_npc_point(npc_roi)
        wx, wy = Window().position()
        Click(wx + npc_x + npc.click_x_shift, wy + npc_y + npc.click_y_shift, process='dclick').make_click()
    
    @staticmethod
    def touch_npc(npc):
        title = get_tempalate_roi(npc)
        Navigator.move_to_npc(title, npc)
        Wait(3).delay()
        title, center = get_npc(npc), window.relative_center()
        while not is_near_npc(title, center):
            title, center = get_npc(npc), window.relative_center()
            Wait(1).delay()
        title = get_npc(npc)
        Navigator.click_at_npc(title, npc)
        return title

    @staticmethod
    def turn_around():
        x, y = Window().center()
        Move().fromTo((x, y), (x + TURN_AROUND_DISTANCE,y))

    @staticmethod
    def go_to_start():
        start = get_tempalate_roi(config.StartPointConfig)
        x, y = window.relative(start_point(start))
        Click(x,y).make_click()
        return start
    
    @staticmethod
    def drag_camera(start, end):
        x,y = window.position()
        sx, sy = start
        ex, ey = end
        Move().fromTo((x + sx, y + sy), (x + ex, y + ey))


def get_npc(npc):
    rect = window.rect
    image = screenshot(rect)
    titleCenter = get_tempalate_roi(npc, image)
    return titleCenter

def get_tempalate_roi(config, image=None):
    rect = Window().rect
    if not image:
        image = screenshot(rect)

    extruder = Extruder(image)
    
    # roi = extruder.get_template_rect(config)
    # import cv2
    # from utils.cv2_utils import show_image
    # import numpy as np
    # rected = np.array(image)
    # rected = cv2.cvtColor(rected, cv2.COLOR_RGB2BGR)
    # rected = cv2.rectangle(rected, roi[:2], (roi[0] + roi[2], roi[1] + roi[3]), 255,2)
    # show_image(rected)
    
    return extruder.get_template_rect(config)
    
def distance(point1, point2):
    import math
    x1,y1 = point1
    x2, y2 = point2
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

def is_near_npc(npc, center, near=180):
    # accept 2 rects
    npc = Rect(npc).center()
    d = distance(npc, center)
    # log = logging.getLogger('navigator')
    log.info('Distance: {0},  npc: {1}, center: {2}'.format(d, npc, center))
    return d <= near

def circus_npc_point(roi):
    x,y,w,h = roi
    center = int(x + w/2)
    return (center, y + h)

def start_point(roi):
    x, y, w, h = roi
    right = x + w
    middle =  int(y + h / 2)
    return (right, middle)
