import pyautogui as pag
from modules.screen.screenshot import mssScreenshotNP
from modules.screen.imageSearch import locateTransparentImageOnScreen
from modules.misc.imageManipulation import adjustImage, pillowToCv2
from modules.misc.appManager import openApp
import time
import cv2
import numpy as np
mw, mh = pag.size()
honeyY = 0
threshold = 0.75
numImages = []
for i in range(10):
    numImages.append(adjustImage("images/misc", f"honey_{i}", "retina"))

openApp("roblox")
time.sleep(1.5)
screen = mssScreenshotNP(mw//2-241, honeyY, 140, 36, True)
screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2GRAY)
numbersRes = []
#get all the numbers and their coordinates
for i,e in enumerate(numImages):
    e = cv2.cvtColor(e, cv2.COLOR_RGB2GRAY)
    res = cv2.matchTemplate(screen,e,cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >=threshold)
    w, h = e.shape[::-1]
    screenCopy = screen.copy()
    #loop through all found coordinates and append it to numberRes
    for pt in zip(*loc[::-1]):
        #cv2.rectangle(screenCopy, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        numbersRes.append((i, pt[0]))
    #cv2.imwrite(f'res{i}.png',screenCopy)

#sort the numbers by their x coordinate
#then extract only the numbers and join them together
numbersRes = int(''.join([str(x[0]) for x in sorted(numbersRes, key=lambda x: x[1])]))
print(numbersRes)
openApp("terminal")
