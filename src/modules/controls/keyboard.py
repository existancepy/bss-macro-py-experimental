import sys
if sys.platform == "win32":
    import pydirectinput as pag
else:
    import pyautogui as pag
import time
#pyautogui without the pause
def press(key, delay = 0.02):
    pag.keyDown(key, _pause = False)
    time.sleep(delay)
    pag.keyUp(key, _pause = False)

#pyautogui with the pause
def slowPress(k):
    pag.keyDown(k)
    time.sleep(0.08)
    pag.keyUp(k)

#recreate natro's tile waiting function
def tileWait(tiles,hasteCap=0):
    try:
        with open("haste.txt","r") as f:
            ws = float(f.read())
        f.close()
    except:
        settings = loadsettings.load()
        ws = settings['walkspeed']
    time.sleep((tiles/8.3)*28/ws)