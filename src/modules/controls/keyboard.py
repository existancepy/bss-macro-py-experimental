import sys
if sys.platform == "win32":
    import pydirectinput as pag
    pag.PAUSE = 0.1
else:
    import pyautogui as pag
import time


class keyboard:
    def __init__(self, walkspeed, haste):
        self.ws = walkspeed
        self.haste = haste

    @staticmethod
    #call the press function of the pag library
    def pagPress(k):
        pag.press(k)
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

    def write(text, interval = 0.1):
        pag.typewrite(text, interval)
    #pyautogui with the pause
    def slowPress(self,k):
        pag.keyDown(k)
        time.sleep(0.08)
        pag.keyUp(k)

    #like press, but with walkspeed and haste compensation
    def walk(self,k,t,applyHaste = True):
        #print(self.haste.value)
        if applyHaste:
            self.press(k,t*28/self.haste.value)
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
    def tileWait(self, tiles,hasteCap=0):
        time.sleep((tiles/8.3)*28/self.haste.value)
    
    def tileWalk(self, key, tiles, applyHaste = True):
        if applyHaste:
            self.press(key,(tiles/8.3)*28/self.ws)
        else:
            self.press(key,(tiles/8.3)*28/self.haste.value)

    #release all movement keys (wasd, space)
    @staticmethod
    def releaseMovement():
        keys = ["w","a","s","d","space"]
        for k in keys:
            keyboard.keyUp(k, False)