import sys
if sys.platform == "win32":
    import pydirectinput as pag
else:
    import pyautogui as pag
import time


class keyboard:
    def __init__(self, walkspeed):
        self.ws = walkspeed

    def keyDown(self, k):
        pag.keyDown(k)

    def keyUp(self, k):
        pag.keyUp(k)

    #pyautogui without the pause
    def press(self,key, delay = 0.02):
        pag.keyDown(key, _pause = False)
        time.sleep(delay)
        pag.keyUp(key, _pause = False)

    #pyautogui with the pause
    def slowPress(self,k):
        pag.keyDown(k)
        time.sleep(0.08)
        pag.keyUp(k)

    #like press, but with walkspeed and haste compensation
    def walk(self,k,t):
        self.press(k,t*28/self.ws)
    #like walk, but with multiple keys
    def multiWalk(self, keys, t):
        for k in keys:
            pag.keyDown(k, _pause = False)
        time.sleep(t*28/self.ws)
        for k in keys:
            pag.keyUp(k, _pause = False)
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
    #release all movement keys (wasd, space)
    def releaseMovement(self):
        keys = ["w","a","s","d","space"]
        for k in keys:
            self.keyUp(k)