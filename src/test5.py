from modules.submacros.hourlyReport import BuffDetector
from modules.screen.screenshot import mssScreenshotNP
import time
import numpy as np
from PIL import Image, ImageOps, ImageEnhance
import cv2
from modules.screen.ocr import ocrRead

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
    "focus": [0xff22ff06, (5,1)],
    "bomb_combo": [0xff272727, (5,1)],
    "balloon_aura": [0xfffafd38, (5,1)],
    "boost": [0xff90ff8e, (5,1)],
    "blue_boost": [0xff56a4e4, (4,2)],
    "red_boost": [0xffe46156, (4,2)]
}

uptimeBuffsValues = {k:[0]*1    for k in uptimeBuffsColors.keys()} #*600
for k in ["bear", "white_boost"]:
    uptimeBuffsValues[k] = [0]
#screen = bd.screenshotBuffArea()
#screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2BGR)
screen = cv2.imread("hah4.png")
#print(bd.getBuffsWithImage(buff, True))
currMin = 0
currSec = 0
i = (60*currMin + currSec)//6
x = 0

for j in ["baby_love"]:
    if buffDetector.detectBuffColorInImage(screen, uptimeBuffsColors[j][0], uptimeBuffsColors[j][1], y1=30*multi, searchDirection=7):
        uptimeBuffsValues[j][i] = 1

bearBuffRes = [int(x) for x in buffDetector.getBuffsWithImage(uptimeBearBuffs, screen=screen)]
print(bearBuffRes)
if any(bearBuffRes):
    uptimeBuffsValues["bear"][i] = 1

for j in ["focus", "bomb_combo", "balloon_aura"]:
    res = buffDetector.detectBuffColorInImage(screen, uptimeBuffsColors[j][0], uptimeBuffsColors[j][1], y1=30*multi, y2=50*multi, searchDirection=7)
    if res:
        x = res[0]+res[2]
        buffImg = screen.copy()[15*multi:50*multi , x-25*multi:x+5*multi]
        uptimeBuffsValues[j][i] = int(buffDetector.getBuffQuantityFromImgTight(buffImg))

x = 0
for _ in range(3):
    res = buffDetector.detectBuffColorInImage(screen, uptimeBuffsColors["haste"][0], uptimeBuffsColors["haste"][1],x, 30*multi, searchDirection=6)
    if not res:
        break
    x = res[0]
    if buffDetector.detectBuffColorInImage(screen, uptimeBuffsColors["melody"][0], uptimeBuffsColors["melody"][1], x+2*multi, 30, x+34*multi, 40*multi, 12):
        uptimeBuffsValues["melody"][i] = 1
    elif not uptimeBuffsValues["haste"][i]:
        buffImg = screen.copy()[15*multi:50*multi , x+6*multi:x+44*multi]
        uptimeBuffsValues["haste"][i] = int(buffDetector.getBuffQuantityFromImgTight(buffImg))
    x += 44*multi
#print(bd.detectBuffColorInImage(screen, 0xff242424, variation=12, minSize=(3*2,2*2), show=True))

x = screen.shape[1]
for _ in range(3):
    res = buffDetector.detectBuffColorInImage(screen, uptimeBuffsColors["boost"][0], uptimeBuffsColors["boost"][1], y1=30*multi, x2=x, searchDirection=7)
    if not res:
        break
    x = res[0]+res[2]
    y = res[1] + res[3]

    if len(buffDetector.detectBuffColorInImage(screen, uptimeBuffsColors["red_boost"][0], uptimeBuffsColors["red_boost"][1], x-30*multi, 15*multi, x-4*multi, 34*multi, 20)):
        buffType = "red_boost"
    elif len(buffDetector.detectBuffColorInImage(screen, uptimeBuffsColors["blue_boost"][0], uptimeBuffsColors["blue_boost"][1], x-30*multi, 15*multi, x-4*multi, 34*multi, 20)):
        buffType = "blue_boost"
    else:
        buffType = "white_boost"

    buffImg = screen[15*multi: 50*multi,x-25*multi: x]
    uptimeBuffsValues[buffType][i] = int(buffDetector.getBuffQuantityFromImgTight(buffImg))

    x -= 40*multi

print(uptimeBuffsValues)