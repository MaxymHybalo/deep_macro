import cv2
import pyautogui as ui
import numpy as np

# colors
COLOR_CANCEL = (200, 0, 0)
COLOR_CAPCHA_ROI = (10, 200, 0)
COLOR_OPTION = (20, 20, 200)
# / colors
EXAMPLE = 'new_capcha.png'
DECLINE = 'assets/decline_exam.png'
CAPCHA_ROI = (483, 300, 320, 220)

OPTIONS_START = (34, 38)
OPTION_SIZE = (247, 22)
OPTINON_GAP = 6

img = cv2.imread(EXAMPLE)
img = img[CAPCHA_ROI[1]:CAPCHA_ROI[1] + CAPCHA_ROI[3], CAPCHA_ROI[0]:CAPCHA_ROI[0] + CAPCHA_ROI[2]]
colored = img.copy()
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
decline = cv2.imread(DECLINE, 0)
result = cv2.matchTemplate(img, decline, cv2.TM_SQDIFF_NORMED)

w, h = decline.shape[::-1]
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

top_left = min_loc
bottom_right = (top_left[0] + w, top_left[1] + h)


def calc_options():
    options = []
    sx, sy = OPTIONS_START
    _, h = OPTION_SIZE
    for i in range(0, 5):
        options.append((sx, sy + h*i + OPTINON_GAP*i))
    return options


print(min_val, max_val, min_loc, max_loc)
# cv2.rectangle(colored, (CAPCHA_ROI[0], CAPCHA_ROI[1]), (CAPCHA_ROI[0] + CAPCHA_ROI[2], CAPCHA_ROI[1] + CAPCHA_ROI[3]), COLOR_CAPCHA_ROI, 2) # capcha
cv2.rectangle(colored,top_left, bottom_right, COLOR_CANCEL, 2) # cancel rect
for o in calc_options(img):
    x, y = o
    print(o)
    cv2.rectangle(colored, (x, y), (x + OPTION_SIZE[0], y + OPTION_SIZE[1]), COLOR_OPTION, 1)
cv2.imwrite('examp_result.png', colored)
cv2.imshow('img', colored)
cv2.waitKey(0)


# from win10toast import ToastNotifier

# toast = ToastNotifier()

# toast.show_toast(
#     "Notification",
#     "Notification body",
#     duration = 20,
#     icon_path = "icon.ico",
#     threaded = True,
# )