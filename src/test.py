import time, cv2
from modules.screen.screenshot import mssScreenshotNP
from modules.misc.imageManipulation import adjustImage
import numpy as np
import pyautogui as pag

mw, mh = pag.size()

time.sleep(3)
honeyY = 0
threshold = 0.75
numImages = []
for i in range(10):
    numImages.append(adjustImage("images/misc", f"honey_{i}", "built-in"))
screen = mssScreenshotNP(mw//2-241, honeyY, 140, 36)
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
        cv2.rectangle(screenCopy, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        numbersRes.append((i, pt[0], res[pt[1]][pt[0]]))
    cv2.imwrite(f'res{i}.png',screenCopy)

print(numbersRes)
#sometimes, the numbers can be matched multiple times at the same coordinates
#this filters them out
#check a number and get all the other values with the same coordinates
#select the one with the highest threshold
numbersFinal = []
while numbersRes:
    target = numbersRes.pop(0)
    bestNumber = target
    for e in numbersRes.copy():
        if abs(e[1] - target[1]) < 4:
            if e[2] > bestNumber[2]:
                bestNumber = e
            numbersRes.remove(e)
    numbersFinal.append(bestNumber)
#sort the numbers by their x coordinate
#then extract only the numbers and join them together
result = ''.join([str(x[0]) for x in sorted(numbersFinal, key=lambda x: x[1])])
print(numbersFinal)
print(result)