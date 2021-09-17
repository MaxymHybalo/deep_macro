import cv2
import pytesseract
print(pytesseract)
img = cv2.imread('numbers.png')
# custom_config = r'--oem 3 --psm 6'
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
text = pytesseract.image_to_string(img)

print(text)