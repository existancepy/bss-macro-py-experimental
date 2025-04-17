import sys
if sys.platform == "win32":
    import pydirectinput as pag
    pag.PAUSE = 0.1
else:
    import pyautogui as pag
import time
from modules.submacros.hasteCompensation import HasteCompensation


class keyboard:
    def __init__(self, walkspeed, haste, enableHasteCompensation):
        self.ws = walkspeed
        self.haste = haste
        self.enableHasteCompensation = enableHasteCompensation
        self.hasteCompensation = HasteCompensation(True, walkspeed)

    @staticmethod
    #call the press function of the pag library
    def pagPress(k):
        pag.press(k)
    @staticmethod
    def keyDown(k, pause = True):
        #for some reason, the function key is sometimes held down, causing it to open the dock or enable dictation
        if sys.platform == "darwin":
            keyboard.keyUp('fn', False)
        pag.keyDown(k, _pause = pause)

    @staticmethod
    def keyUp(k, pause = True):
        pag.keyUp(k, _pause = pause)

    #pyautogui without the pause
    def press(self,key, delay = 0.02):
        keyboard.keyDown(key, False)
        time.sleep(delay)
        keyboard.keyUp(key, False)

    def write(self, text, interval = 0.1):
        pag.typewrite(text, interval)
    #pyautogui with the pause
    def slowPress(self,k):
        pag.keyDown(k)
        time.sleep(0.08)
        pag.keyUp(k)

    def timeWait(self, duration):
        baseSpeed = 28
        targetDistance = baseSpeed * duration  # Total distance the player should travel
        traveledDistance = 0  # Tracks total integrated distance
        startTime = time.perf_counter()
        prevTime = startTime

        while traveledDistance < targetDistance:
            currentTime = time.perf_counter()
            deltaT = deltaT = max(currentTime - prevTime, 1e-6)
            speed = max(self.haste.value, self.ws)
            traveledDistance += speed * deltaT

            prevTime = currentTime
            time.sleep(0.01)

        elapsed_time = time.perf_counter() - startTime
        print(f"current speed: {speed}, original time: {duration}, actual travel time: {elapsed_time}")

    #like press, but with walkspeed and haste compensation
    def walk(self,k,t,applyHaste = True):
        #print(self.haste.value)
        if applyHaste and self.hasteCompensation:
            keyboard.keyDown(k, False)
            self.timeWait(t)
            keyboard.keyUp(k, False)
        else:
            self.press(k, t*28/self.ws)

    #like walk, but with multiple keys
    def multiWalk(self, keys, t):
        for k in keys:
            pag.keyDown(k, _pause = False)
        self.timeWait(t)
        for k in keys:
            pag.keyUp(k, _pause = False)

    #recreate natro's walk function
    def tileWait(self, n, hasteCap=0):
        #self.getMoveSpeed takes too fast to run
        def a():
            st = time.perf_counter()
            a = self.hasteCompensation.getHaste()
            et = time.perf_counter()
            return st, et, a
        freq = 1  # Simulated frequency constant
        d = freq / 8
        l = n * freq * 4

        s, f, v = a()
        d += v * (f - s) 

        st = time.time()
        while d < l:
            prev_v = v
            s, f, v = a()
            d += ((prev_v + v) / 2) * (f - s) 
        
        print(time.time()-st)
    
    def tileWalk(self, key, tiles, applyHaste = True):
        if applyHaste:
            self.keyDown(key, False)
            self.tileWait(tiles)
            self.keyUp(key, False)
        else:
            self.press(key,(tiles/8.3)*28/self.haste.value)

    #release all movement keys (wasd, space)
    @staticmethod
    def releaseMovement():
        keys = ["w","a","s","d","space"]
        for k in keys:
            keyboard.keyUp(k, False)