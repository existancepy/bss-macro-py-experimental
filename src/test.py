import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import mss
import pyautogui as pag
from modules.misc.appManager import openApp
from modules.misc.imageManipulation import adjustImage
from modules.screen.imageSearch import locateTransparentImageOnScreen
import time
mw, mh = pag.size()

def mssScreenshot(x,y,w,h, save = False):
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {"left": int(x), "top": int(y), "width": int(w), "height": int(h)}
        # Grab the data and convert to opencv img
        sct_img = np.array(sct.grab(monitor))
        return sct_img

openApp("Roblox")
time.sleep(2)
st = time.time()
template = adjustImage("./images/menu","makehoney","built-in")
res = locateTransparentImageOnScreen(template, mw//2-200,0,400,mh//8, 0.75)
print(res)