import pytesseract
import cv2
from datetime import datetime

ALPHABET = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
# ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
NUMBERS_AREA = (730, 290, 45, 25)
CHARNAME_AREA = (45, 28, 170, 16)
def crop_roi(img, roi):
	x,y, w,h = roi
	return img[y:y+h, x:x+w]


def pre_process_number_reading(img):
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	ret, th1 = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
	img = th1
	return img


def _prepare_recognizing(img, roi):
	if img is None:
		return None
	img = crop_roi(img, roi)
	img = pre_process_number_reading(img)
	return img


def get_numbers_from_img(img, handle=0):
	img = _prepare_recognizing(img, NUMBERS_AREA)
	# change lang  to specified
	try:
		text = pytesseract.image_to_string(img, config='-c tessedit_char_whitelist=0123456789')
	except:
		print('ERROR IMAGE', img)
		return None
	text = ''.join(text.strip())
	text = text[:3]
	if len(text) > 0:
		imname = str(handle) + '_' + str(datetime.now().strftime('%H_%M_%S')) + '.png'
		print('logs to: ', imname, img.shape)
		cv2.imwrite('logs/' + imname, img)
	print('Tesseract text extracted: ', text, 'length', len(text))
	return text if len(text) == 3 else None


def get_char_name(img):
	img = _prepare_recognizing(img, CHARNAME_AREA)
	text = pytesseract.image_to_string(img, config='-c tessedit_char_whitelist=' + ALPHABET)
	text = ''.join(text.strip())
	print('Tesseract Charname extracted: ', text, len(text))
	return text

# img = cv2.imread('numbers.png')

# text = get_numbers_from_img(img)
# print(text)
# img = crop_roi(img, NUMBERS_AREA)
# img = pre_process_number_reading(img)
# cv2.imshow('res', img)
# cv2.waitKey(0)