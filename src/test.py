from modules.misc.appManager import openApp
from modules.screen.screenshot import mssScreenshot
import pyautogui as pag
mw, mh = pag.size()
import time
openApp("roblox")
time.sleep(1)
mssScreenshot(mw//2-100, mh-10, 200, 10, True)
