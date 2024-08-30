import cv2
from modules.screen.screenshot import mssScreenshot, mssScreenshotNP
import numpy as np

def templateMatch(smallImg, bigImg):
    res = cv2.matchTemplate(bigImg, smallImg, cv2.TM_CCOEFF_NORMED)
    return cv2.minMaxLoc(res)

def locateImageOnScreen(target, x,y,w,h, threshold = 0):
    screen = mssScreenshot(x,y,w,h)
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    _, max_val, _, max_loc = templateMatch(target, screen)
    if max_val < threshold: return None
    return (max_val, max_loc)

#used for locating templates with transparency
#this is done by template matching with the gray color space
def locateTransparentImageOnScreen(target, x,y,w,h, threshold = 0):
    screen = mssScreenshotNP(x,y,w,h)
    
    screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2GRAY)
    target = cv2.cvtColor(target, cv2.COLOR_RGB2GRAY)
    _, max_val, _, max_loc = templateMatch(target, screen)
    print(max_val)
    if max_val < threshold: return None
    return (max_val, max_loc)