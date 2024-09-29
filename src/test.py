import numpy as np
import cv2
from modules.screen.screenshot import mssScreenshot, mssScreenshotNP
from modules.misc.imageManipulation import *
import time
import pyautogui as pag
mw,mh = pag.size()
resetLower1 = np.array([0, 102, 0])  # Lower bound of the color (H, L, S)
resetUpper1 = np.array([40, 255, 7])  # Upper bound of the color (H, L, S)
#balloon color
resetLower2 = np.array([105, 140, 210])  # Lower bound of the color (H, L, S)
resetUpper2 = np.array([120, 220, 255])  # Upper bound of the color (H, L, S)
resetKernel = cv2.getStructuringElement(cv2.MORPH_RECT,(16,10))

time.sleep(3)
screen = pillowToCv2(mssScreenshot(mw//2-100, mh-10, 200, 10))
# Convert the image from BGR to HLS color space
hsl = cv2.cvtColor(screen, cv2.COLOR_BGR2HLS)
# Create a mask for the color range
mask1 = cv2.inRange(hsl, resetLower1, resetUpper1)  
mask2 = cv2.inRange(hsl, resetLower2, resetUpper2)    
mask = cv2.bitwise_or(mask1, mask2)
mask = cv2.erode(mask, resetKernel)
#get contours. If contours exist, direction is correct
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(bool(contours))