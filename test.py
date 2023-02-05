
import pyautogui as pag
import time
import os
import tkinter
import move
import sys
import cv2
from PIL import ImageGrab
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
cmd = """
osascript -e 'activate application "Roblox"' 
"""
os.system(cmd)

time.sleep(1)
savedata = {}
def loadSave():
    with open('save.txt') as f:
        lines = f.read().split("\n")
    f.close()
    for s in lines:
        l = s.replace(" ","").split(":")
        if l[1].isdigit():
            l[1] = int(l[1])
        savedata[l[0]] = l[1]
loadSave()
setdat = loadsettings.load()
ww = savedata["ww"]
wh = savedata["wh"]
ms = pag.size()
mw = ms[0]
mh = ms[1]

def screenshotebutton():
    setdat = loadsettings.load()
    webhook("","Screenshotting: eb.png","dark brown",1)
    xo = ww//2.6
    yo = wh//19
    xt = ww//25
    yt = wh//30
    im = pag.screenshot(region = (xo,yo,xt,yt))
    im.save('eb.png')
    '''
    if setdat['display_type'] ==  "built-in retina display":
        im.save('./images/retina/eb.png')
    else:
        im.save('./images/built-in/eb.png')
    '''


screenshotebutton()
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


