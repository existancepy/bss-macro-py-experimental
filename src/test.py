from modules.misc.appManager import openApp
import time
from modules.screen.screenshot import mssScreenshot
import pyautogui as pag
mw, mh = pag.size()
openApp("Roblox")
time.sleep(2)
mssScreenshot(mw//2+150, 4*mh//10+160, 120, 60)