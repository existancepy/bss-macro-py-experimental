import modules.misc.appManager as appManager
import modules.screen.screenData as screenData
import cv2
import numpy as np
import pyautogui as pag
import modules.controls.keyboard as keyboardModule
from modules.screen.screenshot import mssScreenshot
import time
from pynput.keyboard import Key, Controller
import modules.controls.mouse as mouse
import sys

pynputKeyboard = Controller()
isRetina = False
whirligig = cv2.imread("./images/retina/inventory/whirligig.png")
mw, mh = pag.size()
keyboard = keyboardModule.keyboard(28)

appManager.openApp("roblox")
time.sleep(2)
keyboard.press("\\")
#align with first buff
for _ in range(7):
    keyboard.press("w")
for _ in range(10):
    keyboard.press("a")
#open inventory
if sys.platform == "darwin":
    for _ in range(5):
        keyboard.press("w")
        time.sleep(0.1)
    keyboard.press("s")
    keyboard.press("a")
    time.sleep(0.1)
    keyboard.press("enter")
    time.sleep(0.1)
    keyboard.press("s")
else:
    keyboard.press("s")
    keyboard.press("enter")
    time.sleep(0.3)
    keyboard.press("s")
#scroll up to reset
for _ in range(100):
    pynputKeyboard.press(Key.page_up)
    pynputKeyboard.release(Key.page_up)
time.sleep(0.8)
#scroll down, note the best match
bestScroll, bestX, bestY = None, None, None
valBest = 0
for i in range(20):
    img = mssScreenshot(0, 80, 150, mh-120)
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    res = cv2.matchTemplate(img_cv, whirligig, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(max_val)
    if max_val > valBest:
        valBest = max_val
        bestX, bestY = max_loc
        bestScroll = i
    for j in range(4):
        pynputKeyboard.press(Key.page_down)
        pynputKeyboard.release(Key.page_down)
        if j > 1: time.sleep(0.05)
#scroll to the top
for _ in range(100):
    pynputKeyboard.press(Key.page_up)
    pynputKeyboard.release(Key.page_up)
time.sleep(0.1)
#scroll to item
for _ in range(bestScroll*4):
    pynputKeyboard.press(Key.page_down)
    pynputKeyboard.release(Key.page_down)
    time.sleep(0.02)
#close UI navigation
keyboard.press("\\")
mouse.teleport(bestX//2+20, bestY//2+80+20)
