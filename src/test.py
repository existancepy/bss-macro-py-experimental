#hsv(186, 7.87%, 49.8%)
#hsv(186.67, 7.14%, 49.41%)
#hsv(186, 7.87%, 49.8%)
#hsv(186.67, 7.32%, 48.24%)

#hsv(202.86, 19.63%, 41.96%)
#hsv(202.86, 19.44%, 42.35%)
#hsv(202.86, 19.63%, 41.96%)

import cv2
import numpy as np
from modules.screen.screenshot import mssScreenshotNP
import time


def isNightFloor(hsv):
    #TODO: Add detection for 5 bee gate
    #TODO: Move the ranges and kernel to global/self
    # Create range (clover, 15 bee gate, 10 bee gate)
    lower1 = np.array([80, 15, 114])
    upper1 = np.array([100, 20, 130])
    #Create range(starter fields, spawn, rose)
    lower2 = np.array([99, 45, 102])
    upper2 = np.array([105, 51, 112])

    #might increase kernel size on retina
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(10,10))

    mask1 = cv2.inRange(hsv, lower1, upper1)   
    mask2 = cv2.inRange(hsv, lower2, upper2)   
    #merge the masks
    mask = cv2.bitwise_or(mask1, mask2)
    mask = cv2.erode(mask, kernel, 2)

    #if np.mean = 0, no color ranges are detected, is day, hence return false
    return bool(np.mean(mask))
    imS = cv2.resize(mask, (960, 540)) 
    cv2.imshow("mask",imS)
    cv2.waitKey(0)


screen = mssScreenshotNP(0,0, 100, 100)
# Convert the image from BGRA to HSV
bgr = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
# Convert the image from BGR to HLS color space
#hsv = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
print(isNightFloor(hsv))



'''
#get contours. If contours exist, direction is correct
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if contours:
    return True
'''