
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
from datetime import datetime
import matplotlib.pyplot as plt
import random
from matplotlib.colors import from_levels_and_colors
from matplotlib.collections import LineCollection
import math
from pynput.keyboard import Key, Controller
import pynput
from pynput.mouse import Button
import Quartz.CoreGraphics as CG
import struct
import reset
from pixelcolour import getPixelColor
keyboard = Controller()
mouse = pynput.mouse.Controller()
#import easyocr
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


savedata = loadRes()
ww = savedata['ww']
wh = savedata['wh']

    
roblox()

def detectNight():
    savedat = loadRes()
    ww = savedat['ww']
    wh = savedat['wh']
    ylm = loadsettings.load('multipliers.txt')['y_length_multiplier']
    xlm = loadsettings.load('multipliers.txt')['x_length_multiplier']
    screen = np.array(pag.screenshot(region=(0,0,round((ww/3.4)*xlm),round((wh/25)*ylm))))
    w,h = screen.shape[:2]
    rgb = screen[0,0][:3]
    for x in range(w):
        for y in range(h):
            if list(screen[x,y][:3]) == [0,0,0]:
                success = True
                for x1 in range(5):
                    for y1 in range(5):
                        if not x1 < w and y1 < h:
                            if screen[x1,y1][:3] != (0,0,0):
                                success = False
                if success:
                    print("night detected")
                    return
                
                    
    '''
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    small_image = cv2.imread('./images/general/nightsky.png')
    large_image = screen
    res = cv2.matchTemplate(small_image, large_image, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    x,y = max_loc
    print("Trying to find night sky. max_val is {} ".format(max_val))
    MPx,MPy = min_loc
    
    print(MPx,MPy)
    pag.moveTo(MPx//2,MPy//2)
    # Step 2: Get the size of the template. This is the same size as the match.
    trows,tcols = small_image.shape[:2]
    # Step 3: Draw the rectangle on large_image
    cv2.rectangle(large_image, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,255),2)
    # Display the original image with the rectangle around the match.
    cv2.imshow('output',large_image)
    # The image is only displayed if we call this
    cv2.waitKey(0)

    if max_val >= 0.5:
        return [1,x,y,max_val]
    return
    '''
while True:  
    detectNight()
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


