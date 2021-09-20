import pytesseract
import cv2
from datetime import datetime

NUMBERS_AREA = (605, 290, 80, 30)

def crop_roi(img, roi):
	x,y, w,h = roi
	return img[y:y+h, x:x+w]


def pre_process_number_reading(img):
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	ret, th1 = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
	img = th1
	return img


def get_numbers_from_img(img, handle=0):
	if img is None:
		return None
	img = crop_roi(img, NUMBERS_AREA)
	img = pre_process_number_reading(img)
	# change lang  to specified
	text = pytesseract.image_to_string(img, config='-c tessedit_char_whitelist=0123456789')
	text = ''.join(text.strip())
	text = text[:3]
	if len(text) > 0:
		imname = str(handle) + '_' + str(datetime.now().strftime('%H_%M_%S')) + '.png'
		print('logs to: ', imname, img.shape)
		cv2.imwrite('logs/' + imname, img)
	print('Tesseract text extracted: ', text, 'length', len(text))
	return text if len(text) == 3 else None

# img = cv2.imread('numbers.png')

# text = get_numbers_from_img(img)
# print(text)
# img = crop_roi(img, NUMBERS_AREA)
# img = pre_process_number_reading(img)
# cv2.imshow('res', img)
# cv2.waitKey(0)