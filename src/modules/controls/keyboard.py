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
    
    def getMoveSpeed(self):
        st = time.perf_counter()
        movespeed = self.haste.value
        et = time.perf_counter()
        return st, et, movespeed

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
        base_speed = 28
        target_distance = base_speed * duration  # Total distance the player should travel
        traveled_distance = 0  # Tracks total integrated distance

        start_time = time.perf_counter()
        prev_time = start_time
        _, _, prev_speed = self.getMoveSpeed()

        while traveled_distance < target_distance:
            # Get new speed and current timestamp
            current_time = time.perf_counter()
            _, _, current_speed = self.getMoveSpeed()

            # Compute time difference (delta_t)
            delta_t = current_time - prev_time

            # Apply trapezoidal integration to calculate traveled distance
            traveled_distance += ((prev_speed + current_speed) / 2) * delta_t

            # Update previous values
            prev_time = current_time
            prev_speed = current_speed

        elapsed_time = time.perf_counter() - start_time
        print(f"current speed: {current_speed}, original time: {duration}, actual travel time: {elapsed_time}")

    #like press, but with walkspeed and haste compensation
    def walk(self,k,t,applyHaste = True):
        #print(self.haste.value)
        if applyHaste:
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