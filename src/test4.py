import cv2
from modules.screen.screenshot import mssScreenshot, mssScreenshotNP
import numpy as np
import imagehash
import time
import pyautogui as pag
from modules.misc.imageManipulation import adjustImage

mw, mh = pag.size()
def templateMatch(smallImg, bigImg):
    res = cv2.matchTemplate(bigImg, smallImg, cv2.TM_CCOEFF_NORMED)
    return cv2.minMaxLoc(res)

st = time.time()

target = adjustImage("./images/menu", "mmopen", "retina")
print(f"Adjusted image: {time.time()-st}")
screen = mssScreenshot(0,0,mw,mh)
print(f"Took screenshot: {time.time()-st}")

screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
print(f"Converted to BGR: {time.time()-st}")

templateMatch(target, screen)
print(f"Template match: {time.time()-st}")
print("done")
