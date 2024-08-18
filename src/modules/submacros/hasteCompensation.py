import cv2
import pyautogui as pag
from modules.screen.imageSearch import templateMatch
from modules.screen.screenshot import mssScreenshot
from modules.screen.screenData import getScreenData
import numpy as np
import time
from PIL import Image

isRetina = getScreenData()["display_type"] == "retina"
def adjustBuffImage(path):
    img = Image.open(path)
    #get original size of image
    width, height = img.size
    #if its built-in, half the image
    scaling = 1 if isRetina else 2
    #resize image
    img = img.resize((int(width/scaling), int(height/scaling)))
    #convert to cv2
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

hasteStacks = []
for i in range(10):
    hasteStacks.append(adjustBuffImage(f"./images/general/buffs/haste{i+1}.png"))
hasteStacks = list(enumerate(hasteStacks))[::-1]

bearMorphs = []
for i in range(5):
    bearMorphs.append(adjustBuffImage(f"./images/general/buffs/bearmorph{i+1}.png"))
                       
mw, mh = pag.size()                 
prevHaste = 0
def thresholdMatch(target, screen):
    res = templateMatch(target, screen)
    _, val, _, _ = res
    return (val > 0.7, val)

def hasteCompensation(baseMoveSpeed, haste):
    st = time.time()
    screen = mssScreenshot(0,mh/30,mw/2.1,mh/16)
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    bestHaste = 0
    bestHasteMaxVal = 0
    #match haste
    for i,e in hasteStacks:
        res, val = thresholdMatch(e, screen)
        if res and val > bestHasteMaxVal:
            bestHasteMaxVal = val
            bestHaste = i+1
    #in some cases, 3 and 6 can be detected as 8
    #assume that 8 can also be detected as 3 or 6 and others
    if bestHaste in [3,6,8]:
        if prevHaste == 2:
            bestHaste = 3
        elif prevHaste == 5:
            bestHaste = 6
        else:
            bestHaste = 8
    prevHaste = bestHaste
    #match bear morph
    bearMorph = 0
    for x in bearMorphs:
        res, val = thresholdMatch(x, screen)
        if res:
            print("bear morph active")
            bearMorph = 4
    print(f"Haste stacks: {bestHaste}")
    out = (baseMoveSpeed+bearMorph)*(1+(0.1*bestHaste))
    #print(out)
    haste.value = out

