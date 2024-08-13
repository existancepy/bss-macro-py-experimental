import cv2
from modules.screen.screenshot import mssScreenshot
import numpy as np

def templateMatch(smallImg, bigImg):
    res = cv2.matchTemplate(bigImg, smallImg, cv2.TM_CCOEFF_NORMED)
    return cv2.minMaxLoc(res)

def locateImageOnScreen(target, x,y,w,h):
    screen = mssScreenshot(x,y,w,h)
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    return templateMatch(target, screen)