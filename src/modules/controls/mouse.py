import sys
if sys.platform == "win32":
    import pydirectinput as pag
else:
    import pyautogui as pag
import time
from pynput.mouse import Button, Controller

pynputMouse = Controller()
#move the mouse instantly
def teleport(x,y):
    pag.moveTo(int(x),int(y))

def moveTo(x,y):
    pag.moveTo(int(x),int(y),0.1)

def mouseDown():
    pynputMouse.press(Button.left)
    pag.mouseDown()

def mouseUp():
    pynputMouse.release(Button.left)
    pag.mouseUp()

def moveBy(x = 0,y = 0):
    pag.move(x, y)  

def click():
    mouseDown()
    time.sleep(0.04)
    mouseUp()

def fastClick():
    pynputMouse.press(Button.left)
    pynputMouse.release(Button.left)
