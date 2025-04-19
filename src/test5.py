from modules.submacros.hourlyReport import BuffDetector
from modules.screen.screenshot import mssScreenshotNP
import time
import numpy as np
import cv2

#time.sleep(2)
hourBuffs = {
    "tabby_love": ["top", True, True],
    "polar_power": ["top", True, True],
    "wealth_clock": ["top", True, True],
    "blessing": ["middle", True, True],
    "bloat": ["top", True, True],
}

buff = {
    #"blue_boost": ["middle", True, True],
    # "baby_love": ["middle", True, True],
    "melody": ["top", True, True],
    #"balloon_aura": ["top", True, False]
}

buffDetector = BuffDetector(True, "retina")
multi = 2 if "retina" else 1

uptimeBearBuffs = {
    "bearmorph1": ["top", True, False],
    "bearmorph2": ["top", True, False],
    "bearmorph3": ["top", True, False],
    "bearmorph4": ["top", True, False],
    "bearmorph5": ["top", True, False],
}
uptimeBuffsColors = {
    # "focus": [[np.array([50, 180, 180]), np.array([80, 255, 255])], True, True],
    "baby_love": [0xff8de4f3, (5, 1)],
    "haste": [0xfff0f0f0, (5, 1)],
    "melody": [0xff242424, (3,2)],
}

uptimeBuffsValues = {k:[0]*1 for k in uptimeBuffsColors.keys()} #*600
uptimeBuffsValues["bear"] = [0]
#screen = bd.screenshotBuffArea()
#screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2BGR)
screen = cv2.imread("he.png")
#print(bd.getBuffsWithImage(buff, True))
currMin = 0
currSec = 0
i = (60*currMin + currSec)//6
x = 0

for j in ["baby_love"]:
    if buffDetector.detectBuffColorInImage(screen, uptimeBuffsColors[j][0], uptimeBuffsColors[j][1], y1=30*multi, searchDirection=7):
        uptimeBuffsValues[j][i] = 1

if buffDetector.getBuffsWithImage(uptimeBearBuffs, screen=screen):
    uptimeBuffsValues["bear"][i] = 1

x = 0
for _ in range(3):
    res = buffDetector.detectBuffColorInImage(screen, uptimeBuffsColors["haste"][0], uptimeBuffsColors["haste"][1],x, 30*multi, searchDirection=6)
    if not res:
        break
    x = res[0]
    if buffDetector.detectBuffColorInImage(screen, uptimeBuffsColors["melody"][0], uptimeBuffsColors["melody"][1], x+2*multi, 30, x+34*multi, 40*multi, 12):
        uptimeBuffsValues["melody"][i] = 0
    else:
        print("haste")
        buffImg = screen.copy()
        buffDetector.getBuffQuantityFromImg()
    x += 44*multi
#print(bd.detectBuffColorInImage(screen, 0xff242424, variation=12, minSize=(3*2,2*2), show=True))

print(uptimeBuffsValues)