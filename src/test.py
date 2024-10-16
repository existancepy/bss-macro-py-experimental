'''
import cv2
from PIL import Image

# Load the image
image_path = "test.png"
image = cv2.imread(image_path)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply a threshold to binarize the image (black and white)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Remove noise using a morphological operation (optional for cleaner text)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

cv2.imshow("final", morphed)
cv2.waitKey(0)
'''


from modules.submacros.hourlyReport import getBuffs, getNectars, generateHourlyReport
import time
from modules.misc.appManager import openApp
time.sleep(2)
generateHourlyReport(True)

