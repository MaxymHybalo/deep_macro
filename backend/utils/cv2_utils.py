import logging
import cv2
import pyautogui as ui
import numpy as np

COLOR = (0, 255, 0)
THICKNESS = 1

log = logging.getLogger('image-utils')


def get_image(imagepath):
    if type(imagepath) is str:
        return cv2.imread(imagepath)
    if type(imagepath) in [list, tuple]:
        image = ui.screenshot(region=imagepath)
        image = np.asarray(image)
        return image
    return imagepath


def draw_corners(image, corners, color=255):
    image = get_image(image)
    for c in corners:
        if type(c) not in [tuple, list]:
            x, y = c.ravel()
        else:
            x, y = c
        cv2.circle(image, (x, y), 2, color, 2)
    return image


def rect(image, rect, color=COLOR, thickness=THICKNESS):
    if image is not isinstance(image, np.ndarray):
        image = np.array(image)
    x, y, w, h = rect
    cv2.rectangle(image, (x, y), (x+w, y+h), color, thickness)
    return image


def circle(image, circle, thickness=THICKNESS):
    x, y, r = circle
    cv2.circle(image, (x, y), r, COLOR, thickness)
    return image

def text(image, text, x=0, y=0):
    cv2.putText(image, str(text), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0, 0, 200], 2)
    return image


def make_image(src=None, region=None):
    if region is None:
        image = ui.screenshot(src)
    else:
        if src is not None:
            image = ui.screenshot(src, region=region)
        else:
            image = ui.screenshot(region=region)
    return np.array(image)[:, :, ::-1].copy()


def show(image, name='image'):
    cv2.imshow(name, image)
    width, height = ui.size()
    cv2.moveWindow(name, int(width / 2), int(height / 2))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def draw_rect(image, roi):
    return cv2.rectangle(image, roi[:2], (roi[0] + roi[2], roi[1] + roi[3]), 255,2)

def show_image(image):
    import matplotlib.pyplot as plt
    plt.imshow(image)
    plt.show()


def screenshot(rect):
    import pyautogui as ui
    return ui.screenshot(region=rect)