import math
import cv2
import numpy as np
from world_explorer.utils import cm_triangle, angle_from_triangle
from jobs.helpers.extruder import Extruder
from world_explorer.invariant_template_matching import invariantMatchTemplate

CM_POINTER = 'assets/cam_pointer.png'


CM_X1 = 128 - 40 - 2
CM_X2 = 128 + 40 + 2
CM_Y1 = 128 - 40 - 2
CM_Y2 = 128 + 40 + 2
CENTER = 42
ANGLE_BASE_LINE = [(CENTER, CENTER), (CENTER + 20, CENTER)]

def vector(a, b):
    ax, ay = a
    bx, by = b
    return bx - ax, by - ay

def dot_product(a, b):
    ax, ay = a
    bx, by = b
    return ax*bx + ay*by

def magnitude(a):
    x, y = a
    return math.sqrt(x**2 + y**2)

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def calc_angle(a, b):
    a1, a2 = a
    b1, b2 = b
    vec_a = vector(a1, a2)
    vec_b = vector(b1, b2)
    dotprod = dot_product(vec_a, vec_b)
    mag_a = magnitude(vec_a)
    mag_b = magnitude(vec_b)
    rad = float(dotprod) / float(mag_a * mag_b)
    rad = math.acos(rad)
    _, a2y = a2
    if a2y > CENTER:
        angle = math.degrees(2 * math.pi - rad)
    else:
        angle = math.degrees(rad)
    return rad, angle

def correct_sight(sights):
    start, end = sights
    sx, sy = start
    ex, ey = end
    delta = 13
    dsx = sx - CENTER
    dsy = sy - CENTER
    
    if abs(dsx) < delta and abs(dsy) < delta:
        return [CENTER, CENTER], end
    else:
        return [CENTER, CENTER], start

def camera_angle(img):
    img = img[CM_Y1:CM_Y2, CM_X1:CM_X2]
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([0, 120, 70])   # Lower bound of blue in HSV
    upper_blue = np.array([10, 255, 255]) # Upper bound of blue in HSV
    mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
    red_extracted = cv2.bitwise_and(img, img, mask=mask)
    gray_image = cv2.cvtColor(red_extracted, cv2.COLOR_BGR2GRAY)

    # Parameters for Shi-Tomasi corner detection
    corners = cv2.goodFeaturesToTrack(gray_image, maxCorners=2, qualityLevel=0.01, minDistance=10)
    corners = np.int0(corners)

    # Draw the corners on the original image 
    sights = []
    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(img, (x, y), 5, (0, 255, 0), 1)
        sights.append((x, y))
    # Show the result
    sight_start, sight_end = correct_sight(sights)

    # print(sight_start, sight_end, sights)
    rad, angle = calc_angle([sight_start, sight_end], ANGLE_BASE_LINE)
    # print('Angle', rad, angle)
    return rad, angle
    # cv2.imshow('Image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    