import modules.screen.ocr as ocr
import modules.controls.mouse as mouse
from modules.misc.appManager import openApp
import time
from modules.screen.screenData import getScreenData
openApp("roblox")
time.sleep(1)
multi = 1
screenData = getScreenData()
ww = screenData["screen_width"]
wh = screenData["screen_height"]
region = (ww/3.15,wh/2.15,ww/2.7,wh/4.2)
res = ocr.customOCR(*region,0)
for i in res:
    if "keep" in i[1][0].lower():
        mouse.mouseUp()
        mouse.teleport((i[0][0][0]+region[0])//multi, (i[0][0][1]+region[1])//multi)
        mouse.click()
        breakLoop = True
        break