from modules.screen.screenshot import mssScreenshot
import pyautogui as pag
import time
time.sleep(3)
mw, mh = pag.size()
mssScreenshot(mw/2, mh*2/3, 300, mh/3, True)