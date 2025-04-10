import pyautogui as pag
import time
from modules.screen.screenshot import mssScreenshot
time.sleep(2)
mw, mh = pag.size()
topScreen = mssScreenshot(0, 0, mw, 2)
extrema = topScreen.convert("L").getextrema()
#all are black
if extrema == (0, 0):
    print("a")