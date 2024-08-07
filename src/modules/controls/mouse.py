import sys
if sys.platform == "win32":
    import pydirectinput as pag
else:
    import pyautogui as pag
import time

#move the mouse instantly
def teleport(x,y):
    pag.moveTo(x,y)