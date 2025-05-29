import cv2
from modules.screen.screenshot import mssScreenshot, mssScreenshotNP
import numpy as np
import imagehash
import time

def templateMatch(smallImg, bigImg):
    res = cv2.matchTemplate(bigImg, smallImg, cv2.TM_CCOEFF_NORMED)
    return cv2.minMaxLoc(res)

st = time.time()

screen = mssScreenshot(x,y,w,h)
print(f"Took screenshot: {time.time()-st}")

target = cv2.imread("images/menu/ebutton-retina.png", 0)
screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
print(f"Converted to BGR and got target image: {time.time()-st}")

templateMatch(target, screen)
print(f"Template match: {time.time()-st}")
print("done")
