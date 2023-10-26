import math
import cv2
import numpy as np

from world_explorer.utils import frames, cm_triangle, angle_from_triangle
from jobs.helpers.extruder import Extruder
from world_explorer.invariant_template_matching import invariantMatchTemplate

FILES_PATH = 'logs/world_explorer'
OUT_PATH = 'logs/we_out'

CHAR_POINTER = 'assets/char_pointer1.png'
CM_POINTER = 'assets/cam_pointer.png'

CP_X1 = 129 - 15 - 2
CP_X2 = 129 + 15 + 2
CP_Y1 = 120 - 18 - 2
CP_Y2 = 120 + 18 + 2

CM_X1 = 128 - 15 - 2
CM_X2 = 128 + 15 + 2
CM_Y1 = 128 - 15 - 2
CM_Y2 = 128 + 15 + 2

CP_LOWER = (0,140,0)
CP_UPPER = (255,255,255)

CM_LOWER = (0,0,100)
CM_UPPER = (255,9,255)

# files_count = frames(FILES_PATH)
files_count = 100


black = (255, 255, 255)
WIDTH, HEIGHT = 1286, 797

def find_features(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    corners = cv2.goodFeaturesToTrack(gray, 3, 0.6, 10)
    if isinstance(corners, type(None)):
        return img
    
    corners = np.int0(corners)

    for i in corners:
        x,y = i.ravel()

        cv2.circle(img, (x,y), 3, (255, 100, 20), -1)
    return img

def segmantation(img):
    twoDimage = img.reshape((-1,3))
    twoDimage = np.float32(twoDimage)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 4
    attempts = 5

    ret,label,center=cv2.kmeans(twoDimage,K,None,criteria,attempts,cv2.KMEANS_PP_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()]
    result_image = res.reshape((img.shape))
    return result_image

def hide_panes(img):
    # offset = 27
    offset = 0
    cv2.rectangle(img, (0, offset), (240, 150 + offset), black, -1)
    cv2.rectangle(img, (240, offset), (240 + 240, 70 + offset), black, -1)
    cv2.rectangle(img, (0, 380 + offset), (440, 600 + offset), black, -1)
    cv2.rectangle(img, (0, 600 + offset), (WIDTH, HEIGHT), black, -1)
    return img

def find_pointer(img, lower, upper, pointer, withMatch=True):

    roi = img
    
    e = Extruder(img)
    # cv2.cvtColor(np.uint8([[[84,237, 255]]]), cv2.COLOR_RGB2HSV) cvt pixel to hsv
    hsvImg = e.filterByColor(roi, lower, upper)
    gray = cv2.cvtColor(hsvImg, cv2.COLOR_RGB2GRAY)
    _, threshold = cv2.threshold(gray, 49, 255, cv2.THRESH_BINARY)
    fImg = cv2.bitwise_and(roi, roi, mask = threshold)
    # print(cv2.cvtColor(np.uint8([[[209,211, 212]]]), cv2.COLOR_RGB2HSV))
    
    roi = fImg
    if withMatch is False:
        return roi, threshold
    
    template = cv2.imread(pointer)
    
    res = invariantMatchTemplate(roi, template, 'TM_CCOEFF_NORMED', 0.4, 500, [0,360], 1, [100, 110], 10, True, True)
    return res

def pointer_angle(img):
    rc_roi, rc_th = find_pointer(img[CM_Y1:CM_Y2, CM_X1:CM_X2], CM_LOWER, CM_UPPER, CM_POINTER, withMatch=False)
    rc_th = correct_cam_pointer(img, rc_th)

    contours, hierarchy = cv2.findContours(rc_th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt = []
    for c in contours[0]:
        # cv2.circle(img, c)
        x, y = p = c[0]
        # print('({}, {})'.format(str(x),str(y)))
        # cv2.circle(img, (x + 129, y + 120), 1, (255, 100, 0), 1)
        cnt.append((x,y))

    res, img = cm_triangle(img, cnt, absolute=(98, 89))
    angle, img = angle_from_triangle(res, img)

    a = angle * math.pi / 180
    return a, img

def camera_angle(img):
    r = find_pointer(img[CP_Y1:CP_Y2, CP_X1:CP_X2], CP_LOWER, CP_UPPER, CHAR_POINTER)
    if not len(r):
        return 0, img

    r = r[0]
    _, angle, _ ,k = r
    return angle, img

def correct_cam_pointer(img, threshold):
    e_kernel = np.ones((2,2),np.uint8)
    d_kernel = np.ones((4,4),np.uint8)

    erosion = cv2.erode(threshold, e_kernel, iterations = 2)
    dilation = cv2.dilate(erosion, d_kernel, iterations = 1) 

    return dilation

def adjustImage(img):
    alpha = 2
    beta = 15
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

def search():

    for i in range(files_count):
        # i = 363
        img = '{}/{}.png'.format(FILES_PATH, str(i))
        img = cv2.imread(img)
        originalImg = np.copy(img)
        a, _ = pointer_angle(img)
        # draw pointer assets
        x, y = (129, 119)
        x1 = int(x + 30 * math.cos(a))
        y1 = int(y + 30 * math.sin(a))

        cv2.line(img, (x, y), (x1, y1), (200, 100, 40), 2)
        cv2.circle(img, (x1, y1), 3, (200, 100, 40), -1)
        cv2.rectangle(img, (CM_X1, CM_Y1), (CM_X2, CM_Y2), (120,100, 0), 1)

        angle, _ = camera_angle(img)
        # draw camera angle
        a = angle * math.pi / 180

        length = 20
        x1 = int(x + length * math.cos(a))
        y1 = int(y + length * math.sin(a))
        cv2.circle(img, (x,y) , 20, (0, 0, 255), 1)
        cv2.line(img, (x,y), (x1, y1), (0, 255, 0), 1)
        cv2.circle(img, (x1, y1), 3, (0, 255, 0), -1)
        cv2.putText(img, '{}'.format(str(angle)), (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [250, 190, 200], 1)
        # img = draw_direction_enities(img, res_chr, ((129, 119), (0, 0, 255), 20), ((0, 255, 0), 20))

        h, w, _ = img.shape

        imgSpectre = np.zeros((h*2, w*2,3), np.uint8)
        imgSpectre[0:h,0:w] = img
        imgSpectre[0:h, w:w+w] = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgSpectre[h:h+h,0:w] = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

        cv2.imwrite('{}/{}.png'.format(OUT_PATH, str(i)), imgSpectre)