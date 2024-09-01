import cv2
import pyautogui as pag
from modules.screen.imageSearch import templateMatch
from modules.screen.screenshot import mssScreenshot
from modules.screen.screenData import getScreenData
import numpy as np
import time
from PIL import Image
from modules.misc.imageManipulation import pillowToCv2

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
    return pillowToCv2(img)

hasteStacks = []
for i in range(10):
    hasteStacks.append(adjustBuffImage(f"./images/buffs/haste{i+1}.png"))
hasteStacks = list(enumerate(hasteStacks))[::-1]

bearMorphs = []
for i in range(5):
    bearMorphs.append(adjustBuffImage(f"./images/buffs/bearmorph{i+1}.png"))

hastePlus = adjustBuffImage(f"./images/buff/haste+.png")         
mw, mh = pag.size()                 
prevHaste = 0         
prevHaste368 = 0 #tracking the previous haste to accurately determine if the haste stack is 3,6 or 8
hasteEnds = 0
prevHasteEnds = 0

def thresholdMatch(target, screen):
    res = templateMatch(target, screen)
    _, val, _, _ = res
    return (val > 0.7, val)

def hasteCompensation(baseMoveSpeed, haste):
    global prevHaste368, hasteEnds, prevHasteEnds, prevHaste
    st = time.time()
    screen = pillowToCv2(mssScreenshot(0,mh/30,mw/2.1,mh/16))
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
        if prevHaste368 == 2:
            bestHaste = 3
        elif prevHaste368 == 5:
            bestHaste = 6
        else:
            bestHaste = 8
    elif bestHaste:
        prevHaste368 = bestHaste

    hasteOut = bestHaste
    #failed to detect haste, but the haste is still there (~7.5 secs remaining)
    if not hasteOut:
        currTime = time.time()
        if currTime > hasteEnds and prevHaste: #there is no ongoing hasteEnds
            prevHasteEnds = prevHaste #value to set for the time compensation
            #decrease the countdown for retina (detection is more accurate)
            if isRetina:
                hasteEnds = currTime + (0 if hasteOut == 1 else 2)
            else:
                hasteEnds = currTime + (4 if hasteOut == 1 else 7)
        #there is a hasteEnd ongoing
        if currTime < hasteEnds:
            hasteOut = prevHasteEnds

    prevHaste = bestHaste
     
    #match bear morph
    bearMorph = any(thresholdMatch(x, screen)[0] for x in bearMorphs)
    if bearMorph: 
        bearMorph = 4
        #print("bear morph active")
    
    #match haste+
    if thresholdMatch(hastePlus, screen):
        hasteOut += 2
    #if hasteOut: print(f"Haste stacks: {hasteOut}")
    out = (baseMoveSpeed+bearMorph)*(1+(0.1*hasteOut))
    haste.value = out

