
import pyautogui as pag
import time
import os
import tkinter
import move
import sys
import cv2
from PIL import ImageGrab, Image
import numpy as np
import imagesearch
import loadsettings
import subprocess
import tkinter as tk
import tty
from tkinter import ttk
import backpack
from webhook import webhook
import webbrowser
import reset
import _darwinmouse as mouse
import ast
import getHaste
import pytesseract
from datetime import datetime
import matplotlib.pyplot as plt
import random
from matplotlib.colors import from_levels_and_colors
from matplotlib.collections import LineCollection
import math

def roblox():
    cmd = """
    osascript -e 'activate application "Roblox"' 
    """
    os.system(cmd)
    time.sleep(1)
def loadRes():
    outdict =  {}
    with open('save.txt') as f:
        lines = f.read().split("\n")
    f.close()
    for s in lines:
        l = s.replace(" ","").split(":")
        if l[1].isdigit():
            l[1] = int(l[1])
        outdict[l[0]] = l[1]
    return outdict

#roblox()
savedata = loadRes()
ww = savedata['ww']
wh = savedata['wh']

def imToString(m):
    savedata = loadRes()
    ww = savedata['ww']
    wh = savedata['wh']
    ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
    xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
    # Path of tesseract executable
    #pytesseract.pytesseract.tesseract_cmd ='**Path to tesseract executable**'
    # ImageGrab-To capture the screen image in a loop. 
    # Bbox used to capture a specific area.
    if m == "bee bear":
        cap = pag.screenshot(region=(ww//(3*xsm),wh//(20*ysm),ww//3,wh//7))
    elif m == "egg shop":
        cap = pag.screenshot(region=(ww//(1.2*xsm),wh//(3*ysm),ww-ww//1.2,wh//5))
    elif m == "ebutton":
        cap = pag.screenshot(region=(ww//(2.65*xsm),wh//(20*ysm),ww//21,wh//17))
        img = cv2.cvtColor(np.array(cap), cv2.COLOR_RGB2BGR)
        img = cv2.resize(img, None, fx=2, fy=2)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        config = '--oem 3 --psm %d' % 10
        tesstr = pytesseract.image_to_string(img, config = config, lang ='eng')
        return tesstr
    elif m == "honey":
        cap = pag.screenshot(region=(ww//(3*xsm),0,ww//6.5,wh//25))
        img = cv2.cvtColor(np.array(cap), cv2.COLOR_RGB2BGR)
        gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        (h, w) = gry.shape[:2]
        gry = cv2.resize(gry, (w * 2, h * 2))
        (T, threshInv) = cv2.threshold(gry, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        tesstr = pytesseract.image_to_string(threshInv, config = "digits")
        tessout = ""
        for i in tesstr:
            if i.isdigit():
                tessout += i
            elif i == "(" or i == "[" or i == "{":
                break
        print(millify(int(tessout)))
        return tessout
    elif m == "disconnect":
        cap = pag.screenshot(region=(ww//3,wh//2.8,ww//2.3,wh//2.5))
    # Converted the image to monochrome for it to be easily 
    # read by the OCR and obtained the output String.
    tesstr = pytesseract.image_to_string(cv2.cvtColor(np.array(cap), cv2.COLOR_BGR2GRAY), lang ='eng')
    return tesstr

def checkwithOCR(m):
    text = imToString(m).lower()
    if m == "bee bear":
        if "bear" in text:
            return True
    elif m == "egg shop":
        if "bee egg" in text or "basic bee" in text or "small bag" in text or ("blue" in text and "bubble" in text):
            return True
    elif m == "disconnect":
        if "disconnected" in text.lower():
            return True
    return False
def millify(n):
    millnames = ['',' K',' M',' B',' T', 'Qd']
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.2f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

def hourlyReport(hourly=1):
    setdat = loadsettings.load()
    with open('honey_history.txt','r') as f:
        honeyHist = ast.literal_eval(f.read())
    f.close()
    if honeyHist.count(honeyHist[0]) != len(honeyHist):
        for i, e in reversed(list(enumerate(honeyHist[:]))):
            if e != setdat['prev_honey']:
                break
            else:
                honeyHist.pop(i)
    print(honeyHist)
    while True:
        #print([millify(x) for x in honeyHist])
        compList = honeyHist.copy()
        sortedHoney = sorted(compList)
        if sortedHoney == compList:
            break
        else:
            removeELE = sortedHoney[-1]
            honeyHist.remove(removeELE)
    print(honeyHist)
    currHoney = honeyHist[-1]
    session_honey = currHoney - setdat['start_honey']
    hourly_honey = currHoney - setdat['prev_honey']
    if hourly:
        loadsettings.save('prev_honey',currHoney)
        timehour = int(datetime.now().hour) - 1
    else:
        timehour = int(datetime.now().hour)
        
    stime = time.time() - setdat['start_time']
    day = stime // (24 * 3600)
    stime = stime % (24 * 3600)
    hour = stime // 3600
    stime %= 3600
    minutes = stime // 60
    stime %= 60
    seconds = round(stime)
    session_time = "{}d {}h {}m".format(round(day),round(hour),round(minutes))
    yvals = []
    for i in range(len(honeyHist)):
        if i != 0:
            hf, hb = honeyHist[i], honeyHist[i-1]
            yvals.append(int(hf) - int(hb))
    #yvals = [1,2,3,4,5,6,7,8]
    xvals = [x+1 for x in range(len(yvals))]


    fig = plt.figure(figsize=(12,12), dpi=60,constrained_layout=True)
    gs = fig.add_gridspec(12,12)
    fig.patch.set_facecolor('#121212')

    axText = fig.add_subplot(gs[0:12, 8:12])
    axText.get_xaxis().set_visible(False)
    axText.get_yaxis().set_visible(False)
    axText.patch.set_facecolor('#121212')
    axText.spines['bottom'].set_color('#121212')
    axText.spines['top'].set_color('#121212')
    axText.spines['left'].set_color('#121212')
    axText.spines['right'].set_color('#121212')

    plt.text(0.3,1,"Report", fontsize=20,color="white")
    plt.text(0,0.95,"Session Time: {}".format(session_time), fontsize=15,color="white")
    plt.text(0,0.90,"Session Honey: {}".format(millify(session_honey)), fontsize=15,color="white")
    plt.text(0,0.85,"Honey/Hr: {}".format(millify(hourly_honey)), fontsize=15,color="white")

    ax1 = fig.add_subplot(gs[0:3, 0:7])
    if max(yvals) == 0:
        yticks = [0]
    else:
        yticks = np.arange(0, max(yvals)+1, max(yvals)/4)
    yticksDisplay = [millify(x) if x else x for x in yticks]

    xticks = np.arange(0,max(xvals)+1, 10)
    xticksDisplay = ["{}:{}".format(timehour,x) if x else "{}:00".format(timehour) for x in xticks]

    ax1.set_yticks(yticks,yticksDisplay,fontsize=16)
    ax1.set_xticks(xticks,xticksDisplay,fontsize=16)
    ax1.set_title('Honey/min',color='white',fontsize=19)
    ax1.patch.set_facecolor('#121212')
    ax1.spines['bottom'].set_color('white')
    ax1.spines['top'].set_color('white')
    ax1.spines['left'].set_color('white')
    ax1.spines['right'].set_color('white')
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    ax1.plot(xvals, yvals,color="#BB86FC")
    #ax1.fill_between(xvals, 0, yvals)
    '''
    ax2 = fig.add_subplot(gs[4:7, 0:7])
    y2ticks = np.linspace(setdat['start_honey'], max(honeyHist), num = 4)
    y2ticksDisplay = [millify(x) if x else x for x in y2ticks]
    ax2.set_xticks(xticks,xticksDisplay,fontsize=16)
    ax2.set_yticks(y2ticks,y2ticksDisplay,fontsize=16)
    ax2.set_title('Session honey',color='white',fontsize=19)
    ax2.patch.set_facecolor('#121212')
    ax2.spines['bottom'].set_color('white')
    ax2.spines['top'].set_color('white')
    ax2.spines['left'].set_color('white')
    ax2.spines['right'].set_color('white')
    ax2.tick_params(axis='x', colors='black')
    ax2.tick_params(axis='y', colors='white')
    ax2.plot(xvals, honeyHist[1:],color="#BB86FC")
    #ax2.fill_between(xvals, setdat['start_honey'], honeyHist[1:])
    '''
    print(honeyHist)
    plt.grid(alpha=0.08)
    plt.savefig("hourlyReport.png", bbox_inches='tight')    
    c = Image.open("hourlyReport.png")
    d = c.resize((1452,1452),resample = Image.BOX)
    d.save("hourlyReport-resized.png")
    webhook("**Hourly Report**","","light blue",0,1)

hourlyReport(0)

'''

times = []
start = time.time()
for _ in range(5):
    start = time.time()
    move.press(",")
    move.press("e")
    time.sleep(0.8)
    pag.keyDown("w")
    move.press("space")
    move.press("space")
    time.sleep(9)
    pag.keyUp("w")
    move.press("space")
    times.append(time.time()-start)
print(sum(times)/len(times))
'''

'''
# For both Python 2.7 and Python 3.x
from PIL import Image
img_data = b'iVBORw0KGgoAAAANSUhEUgAAAJ8AAAAWAQMAAADkatyzAAAABlBMVEUAAAAbKjWMzP1VAAAAAXRSTlMAQObYZgAAAdlJREFUeAEBzgEx/gD4AAAAAAAAAAAAAAAAAAAAAAAAAAD+BgAAAAAADAAAAAHgDAAAAEAAAAD/BgAAAAB+DAAAAAH+DAAAAEAAAACBhgAAAACCDAAAAAECDAAAAEAAAACBhgAAAAGADAAAAAEDDAAAAEAAAACBhjBAAAGADB8MDAEDDB8MAfAAJgCBBjBB8AEADAGEDAEDDAGP4fD4PAD/BjBCCAEADACECAH+DACMEEEEMAD+BjBCCAEADACGGAHgDACMEEEEIAD/BjBD+AEADB+CEAEADB+MEEH8IACBhjBH/AEADCCCEAEADCCMEEP+IACAhjBGAAGADCCDMAEADCCMEEMAIACAhhBCAAGADCCBIAEADCCMEEEAIACBhhBCAACCDCCB4AEADCCMEEEAIAD/Bg/B8AB+DB+AwAEADB+MEHD4IAD4BgAAAAAADAAAwAEADAAMEAAAIAAAAAAAAAAAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAADAAAAAAAAAAAAAFzEPdK0OEUMAAAAAElFTkSuQmCC'
import base64
with open("imageToSave.png", "wb") as fh:
    fh.write(base64.decodebytes(img_data))
c = Image.open("imageToSave.png")
d = c.resize((1000,700), resample=Image.BOX)
d.show()

'''


