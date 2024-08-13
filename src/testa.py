import modules.misc.appManager as appManager
import modules.screen.screenData as screenData
import cv2
import numpy as np
import pyautogui as pag
import modules.controls.keyboard as keyboardModule
from modules.screen.screenshot import mssScreenshot
import time
import pyscreeze
pyscreeze.locateAll = pyscreeze._locateAll_pillow
from pynput.keyboard import Key, Controller
import modules.controls.mouse as mouse

pynputKeyboard = Controller()
whirligig = cv2.imread("./whirligig.png")
mw, mh = pag.size()
keyboard = keyboardModule.keyboard(28)

appManager.openApp("roblox")
time.sleep(2)
keyboard.press("\\")
#align with first buff
for _ in range(20):
    keyboard.press("a")
for _ in range(7):
    keyboard.press("w")
#open inventory
for _ in range(2):
    keyboard.press("s")
    time.sleep(0.3)

#scroll down, note the best match
bestScroll, bestX, bestY = None, None, None
valBest = 0
for i in range(20):
    for _ in range(4):
        pynputKeyboard.press(Key.page_down)
        pynputKeyboard.release(Key.page_down)
        time.sleep(0.1)
    img = mssScreenshot(0,80,100,mh-160)
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    res = cv2.matchTemplate(img_cv, whirligig, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val > valBest:
        valBest = max_val
        bestX, bestY = max_loc
        bestScroll = i+1
#scroll to the top
for _ in range(100):
    pynputKeyboard.press(Key.page_up)
    pynputKeyboard.release(Key.page_up)
#scroll to item
for _ in range(bestScroll*4):
    pynputKeyboard.press(Key.page_down)
    pynputKeyboard.release(Key.page_down)
    time.sleep(0.1)
#close UI navigation
keyboard.press("\\")
mouse.teleport(bestX, bestY+80)