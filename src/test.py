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
import pyautogui as pag
from modules.screen.imageSearch import locateImageOnScreen
from modules.misc.imageManipulation import adjustImage
import time
import modules.controls.mouse as mouse

time.sleep(2)
mw, mh = pag.size()
permissionPopup = adjustImage("./images/mac", "allow", "retina")
x = mw/4
y = mh/3
res = locateImageOnScreen(permissionPopup, x, y, mw/2, mh/3, 0.8)
if res:
    x2, y2 = res[1]
    x2 /= 2
    y2 /= 2
    mouse.moveTo(x+x2, y+y2)
    time.sleep(0.08)
    mouse.moveBy(1,1)
    time.sleep(0.1)
    mouse.click()