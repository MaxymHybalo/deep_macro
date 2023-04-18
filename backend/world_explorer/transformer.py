import cv2
import numpy as np
from world_explorer.utils import frames

FILES_PATH = 'logs/world_explorer'
OUT_PATH = 'logs/we_out'

files_count = frames(FILES_PATH)
print(files_count)

black = (255, 255, 255)
WIDTH, HEIGHT = 1286, 797

def find_features(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    corners = cv2.goodFeaturesToTrack(gray, 100, 0.9, 25)
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

def search():

    for i in range(files_count):
        img = '{}/{}.png'.format(FILES_PATH, str(i))
        img = cv2.imread(img)
        # img = hide_panes(img)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # img = find_features(img)
        # img = segmantation(img)
        cv2.imwrite('{}/{}.png'.format(OUT_PATH, str(i)), img)