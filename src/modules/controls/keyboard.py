import sys
if sys.platform == "win32":
    import pydirectinput as pag
else:
    import pyautogui as pag
import time


class keyboard:
    def __init__(self, walkspeed, haste):
        self.ws = walkspeed
        self.haste = haste

    @staticmethod
    def keyDown(k, pause = True):
        pag.keyDown(k, _pause = pause)

    @staticmethod
    def keyUp(k, pause = True):
        pag.keyUp(k, _pause = pause)

    #pyautogui without the pause
    def press(self,key, delay = 0.02):
        keyboard.keyDown(key, False)
        time.sleep(delay)
        keyboard.keyUp(key, False)

    #pyautogui with the pause
    def slowPress(self,k):
        pag.keyDown(k)
        time.sleep(0.08)
        pag.keyUp(k)

    #like press, but with walkspeed and haste compensation
    def walk(self,k,t,applyHaste = True):
        #print(self.haste.value)
        if applyHaste:
            #move at 0.1s increments to adjust to haste mid-movement
            for _ in range(t//0.1):
                self.press(k,0.1*28/self.haste.value)
        else:
            self.press(k, t*28/self.ws)
    #like walk, but with multiple keys
    def multiWalk(self, keys, t):
        for k in keys:
            pag.keyDown(k, _pause = False)
        time.sleep(t*28/self.haste.value)
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
    @staticmethod
    def releaseMovement():
        keys = ["w","a","s","d","space"]
        for k in keys:
            keyboard.keyUp(k, False)