import cv2
import numpy as np
import sys,os
import time
import math

sys.path.insert(0, os.getcwd())

from screen_reader import get_window_image
from driver import click, double, slide, press
from angle import camera_angle, sight_points, calc_angle, ANGLE_BASE_LINE
from world_explorer.utils import window_center, levenshtein_ratio_and_distance, find_npc, find_entry
from ocr import get_text

handle = 1247980
x, y = window_center(handle)
ACC = 2 # how accurate angle
SLIDE_DELTA = 3
RETURN_SCROLL = 'return_scroll.png'
BOSSES = {
    'first': 'Хранитель врат',
    'second': 'Ужасный таркин'
}
BREAK_POINTS = {
    'first': 'first_boss_breakpoint.png',
    'second': 'second_boss_correction_1.png'
}

CORRECTORS = {
    'first': (133, 1),
    'second': (133, 21)
}

HP_END = (649, 67)
HP_COLOR = [63, 5, 198]

def in_bounds(value, bounding, delta=2): # is value in setted bounds with ACC delta
    if value <= bounding + delta and value >= bounding - delta:
        return True
    else:
        return False

def slide_at_angle(angle):
    img = get_image(handle)
    _, curr_a = current_angle(img)
    print(in_bounds(curr_a, angle))
    dx = SLIDE_DELTA if curr_a < angle else -SLIDE_DELTA
    while in_bounds(curr_a, angle) == False:
        slide(x, y, x + dx, y, handle)
        img = get_image(handle)
        _, curr_a = current_angle(img)
        # time.sleep(0.001)
    print('Final Angle', curr_a)

def slide_at_line(sight_point):
    delta = 1
    img = get_image(handle)
    img = sight_roi(img)
    sight_p = sight_points(img, 128)
    cam = sight_p[1]
    line_diff, is_p_o_line = is_point_on_line(cam, sight_point)
    dx = delta if line_diff > 0 else -delta
    while is_point_on_line(cam, sight_point)[1] == False:
        slide(x, y, x + dx, y, handle)
        img = get_image(handle)
        img = sight_roi(img)
        sight_p = sight_points(img, 128)
        cam = sight_p[1]
        print('Slide to line tick ', cam)
    print('End slide at line', cam, sight_p)
def move_forward():
    click(x, y - 100, handle)
    time.sleep(0.8)

def sight_roi(img):
    return img[50 + 1:308 - 2, 1024 + 3:1286 - 3] # change for diff resolution

def get_image(handle):
    img = get_window_image(handle)
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    return img

def current_angle(img):
    mini_map = sight_roi(img)
    return camera_angle(mini_map)

def killed():
    img = get_image(handle)
    hp_bar = img[HP_END[1], HP_END[0]]
    if (hp_bar == HP_COLOR).all():
        return False
    return True

def fight():
    print('Start Fight')
    while killed() == False:
        press(handle, '1')
        time.sleep(0.1)
        press(handle, '2')
        time.sleep(0.1)
        press(handle, '3')
        time.sleep(0.1)
        press(handle, '4')
        time.sleep(0.1)
    press(handle, '4')
    print('End Fight')

def find_target(name):
    press(handle, 'tab')
    time.sleep(0.1)
    img = get_image(handle)
    target_name_roi = img[25 + 1:49, 670:800]
    target_name_roi = cv2.cvtColor(target_name_roi, cv2.COLOR_BGR2GRAY)
    text = get_text(target_name_roi)
    print(text)
    ratio = 0
    if text:
        ratio = levenshtein_ratio_and_distance(text, name, ratio_calc=True)
    print(ratio)
    if ratio > 0.8:
        fight()
    else:
        press(handle, 'tab')
        find_target(name)

def find_breakpoint(template):
    tmp = cv2.imread('./assets/world_explorer/' + template)
    img = get_image(handle)
    img = sight_roi(img)
    return find_entry(img, tmp)

def sight_point(breakpoint, delta):
    x,y = breakpoint
    dx, dy = delta
    return x + dx, y + dy

def ray(direction, x):
    dx, dy = direction
    bx, by = [128, 128]
    m = (dy - by) / (dx - bx)
    b = by - m * bx
    print('Ray', m, b)
    return m * x + b

def is_point_on_line(cam_point, direction_point, tolerance=1):
    # Calculate y based on x0 using the line equation y = mx + b
    y_calculated = ray(direction_point, cam_point[0])
    # Check if the difference between y0 and the calculated y is within a small tolerance
    return y_calculated - cam_point[1], abs(y_calculated - cam_point[1]) < tolerance

def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def dungeon_exit():
    tmp = cv2.imread('./assets/world_explorer/' + RETURN_SCROLL)
    img = get_image(handle)
    x,y = find_entry(img, tmp)
    print('Exit', x,y)
    w, h = (37, 20)
    time.sleep(0.5)
    click(int(x + w / 2), int(y -20 + h / 2), handle) # return scoll position
    time.sleep(0.5)
    click(int(x + w / 2), int(y -20 + h / 2), handle) # return scoll position

    time.sleep(13)

def proceed_npc():
    img = get_image(handle)
    x, y = find_npc(img)
    click(x, y - 25, handle)
    time.sleep(0.1)
    click(x, y - 25, handle)
    time.sleep(1.5)
    tmp = cv2.imread('./assets/world_explorer/enter_dungeon.png')
    x, y = find_entry(img, tmp)
    if y > 200:
        click(x, y - 12, handle)
    else:
        img = get_image(handle)
        x, y = find_npc(img)
        click(x, y - 25, handle)
        time.sleep(0.1)
        click(x, y - 25, handle)
    time.sleep(0.3)
    img = get_image(handle)
    tmp1 = cv2.imread('./assets/world_explorer/enter_dungeon_1.png')
    tmp = cv2.imread('./assets/world_explorer/enter_dungeon.png')

    x, y = find_entry(img, tmp1)
    if y > 200:
        click(x, y - 12, handle)
    else:
        x, y = find_entry(img, tmp)
        click(x, y - 12, handle)

    print('tmp 1', x, y)
    time.sleep(0.5)
    click(685, 415, handle)

# move to 1th boss
def dungeon_loop():
    for i in range(18):
        slide_at_angle(320.0)
        move_forward()
    # find boss
    find_target(BOSSES['first'])
    # First correction
    bp = find_breakpoint(BREAK_POINTS['first'])
    print('Break Point', bp)
    sp = sight_point(bp, CORRECTORS['first'])
    slide_at_line(sp)
    dis = distance([128, 128], sp)
    for _ in range(int(dis / 10)):
        move_forward()
    # End first correction
    # move to 2nd boss
    for i in range(15):
        slide_at_angle(317.6)
        move_forward()
    # # correct positon remove targets
    bp = find_breakpoint(BREAK_POINTS['second'])
    print('Break point, ', bp)
    sp = sight_point(bp, CORRECTORS['second'])
    print('Sight point', sp)
    slide_at_line(sp)

    # img = get_image(handle)
    # img = sight_roi(img)
    # cv2.line(img, [128, 128], sp, [1,100, 243], 1)
    
    # cv2.circle(img, sp, 3,(244,200,0), 1)
    # cv2.circle(img, (136, 133), 4,(144,150,0), 2)
    # cv2.circle(img, (152, 149), 3,(244,0,100), 1)

    # cv2.rectangle(img, bp, [bp[0] + 15, bp[1] + 15], [0,215, 21], 1)
    # cv2.imshow('Image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    for i in range(10):
        # slide_at_angle(321.3)
        move_forward()
    for i in range(4):
        slide_at_angle(347.6)
        move_forward()
    print('START 10 steps')
    for i in range(10):
        slide_at_angle(323.8)
        move_forward()
    for i in range(3):
        slide_at_angle(288.4)
        move_forward()

    find_target(BOSSES['second'])

    dungeon_exit()
    slide_at_angle(293.5)
    for i in range(7):
        move_forward()
    proceed_npc()
    time.sleep(1.5)

for i in range(3):
    dungeon_loop()
# proceed_npc()
img = get_image(handle)
print(current_angle(img))
# sight_p = sight_points(img)
# cam = sight_p[1]
# print('cam', cam)
# bp = find_breakpoint(BREAK_POINTS['first'])
# sp = sight_point(bp, CORRECTORS['first'])

# line_diff, is_p_o_line = is_point_on_line(cam, sp)

# print(bp, sp, is_p_o_line)
# dis = distance([128, 128], sp)
# print('dis', dis)
# cv2.circle(img, sp, 3, (255, 255, 0), 1)
# cv2.circle(img, cam, 3, (255, 255, 0), 1)

# cv2.line(img, [128, 128], sp, (255, 255, 0), 1)

# cv2.imshow('Image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()