import cv2
import pyautogui as pag
from modules.screen.imageSearch import templateMatch
from modules.screen.screenshot import mssScreenshot
import numpy as np
import time
from PIL import Image

def adjustBuffImage(path):
    img = Image.open(path)
    #get original size of image
    width, height = img.size
    #calculate the scaling value (based on width)
    scaling = 1
    #resize image
    img = img.resize((int(width/scaling), int(height/scaling)))
    #convert to cv2
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
    #run a path. Ch
    
hasteStacks = []
for i in range(10):
    hasteStacks.append(adjustBuffImage(f"./images/general/buffs/haste{i+1}.png"))
hasteStacks = list(enumerate(hasteStacks))[::-1]

bearMorphs = []
for i in range(5):
    bearMorphs.append(adjustBuffImage(f"./images/general/buffs/bearmorph{i+1}.png"))
                       
mw, mh = pag.size()                 
print(pag.size())

def thresholdMatch(target, screen):
    res = templateMatch(target, screen)
    _, val, _, _ = res
    return (val > 0.7, val)

while True:
    st = time.time()
    screen = mssScreenshot(0,mh/30,mw/2.1,mh/16)
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    bestHaste = 0
    bestHasteMaxVal = 0
    for i,e in hasteStacks:
        res, val = thresholdMatch(e, screen)
        if res and val > bestHasteMaxVal:
            bestHasteMaxVal = val
            bestHaste = i+1
            
    bearMorph = 0
    for x in bearMorphs:
        res, val = thresholdMatch(x, screen)
        if res:
            #print("bear morph detected")
            bearMorph = 4
    
    out = (29+bearMorph)*(1+(0.1*bestHaste))
    print(out)

