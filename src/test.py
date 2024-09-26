import modules.screen.ocr as ocr
from modules.misc.appManager import openApp
import time
from modules.screen.screenshot import mssScreenshot
import pyautogui as pag
import re

def cdTextToSecs(rawText, brackets):
        if brackets:
            closePos = rawText.find(")")
            #get cooldown if close bracket is present or not
            if closePos >= 0:
                cooldownRaw = rawText[rawText.find("(")+1:closePos]
            else:
                cooldownRaw = rawText.split("(")[1]
        else:
            cooldownRaw = rawText
        #clean it up, extract only valid characters
        cooldownRaw = ''.join([x for x in cooldownRaw if x.isdigit() or x == ":" or x == "s"])
        cooldownSeconds = None #cooldown in seconds

        #check if its days, hour, mins or seconds
        if cooldownRaw.count(":") == 3: #days
            d, hr, mins, s = [int(x) for x in cooldownRaw.split(":")]
            cooldownSeconds = d*24*60*60, hr*60*60 + mins*60 + s
        elif cooldownRaw.count(":") == 2: #hours
            hr, mins, s = [int(x) for x in cooldownRaw.split(":")]
            cooldownSeconds = hr*60*60 + mins*60 + s
        elif cooldownRaw.count(":") == 1: #mins
            mins, s = [int(x) for x in cooldownRaw.split(":")]
            cooldownSeconds = mins*60 + s
        elif "s" in cooldownRaw: #seconds
            cooldownSeconds = int(''.join([x for x in cooldownRaw if x.isdigit()]))
        return cooldownSeconds

mw, mh = pag.size()
openApp("roblox")
time.sleep(1)
x = mw//2-275
y = 4*mh//10
screen = mssScreenshot(x+550/2,y,550/2,40, True)
ocrRes = ''.join([x[1][0] for x in ocr.ocrRead(screen)])
ocrRes = re.findall(r"\(.*?\)", ocrRes)
finalTime = None
if ocrRes:
    times = []
    if "x" in ocrRes[0]: #number of stickers
        stickerCount = int(''.join([x for x in ocrRes[0] if x.isdigit()]))
        times.append(15*60 + 10*stickerCount)
        ocrRes.pop(0)
    if ":" in ocrRes[0]: #direct
        times.append(cdTextToSecs(ocrRes[0], True))
    if times:
        finalTime = max(times)

openApp("Terminal")