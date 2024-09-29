import numpy as np
import cv2
from modules.screen.screenshot import mssScreenshot, mssScreenshotNP
from modules.misc.imageManipulation import *
import time
import pyautogui as pag
from PIL import Image
mw,mh = pag.size()
canDetectNight = True
location = "spawn"
time.sleep(3)
def detectNight():
    #detects the average brightness of the screen. This isn't very reliable since things like lights can mess it up
    #the threshold isnt accurate
    def isNightBrightness(hsv):
        vValues = np.sum(hsv[:, :, 2])
        area = hsv.shape[0] * hsv.shape[1]
        avg_brightness = vValues/area
        print(avg_brightness)
        return 10 < avg_brightness < 120 #threshold for night. It must be > 10 to deal with cases where the player is inside a fruit or stuck against a wall 

    #Detect the color of the floor at spawn
    #Useful when resetting/converting
    def isSpawnFloorNight(hsv):
        lower = np.array([99, 45, 102])
        upper = np.array([105, 51, 112])

        #might increase kernel size on retina
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(15,15))

        mask = cv2.inRange(hsv, lower, upper)   
        mask = cv2.erode(mask, kernel, 2)

        #if np.mean = 0, no color ranges are detected, is day, hence return false
        return np.mean(mask)

    def isNightSky(bgr):
        y = 30
        y*=2
        #crop the image to only the area above buff
        bgr = bgr[0:y, 0:int(mw)]
        w,h = bgr.shape[:2]
        #check if a 15x15 area that is entirely black
        for x in range(w-15):
            for y in range(h-15):
                area = bgr[x:x+15, y:y+15]
                if np.all(area == [0, 0, 0]):
                    return True
        return False

    #detect the color of the grass in fields
    #useful when gathering
    def isGrassNight(hsv):
        def threshold(lower, upper):
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(4,4))
            mask = cv2.inRange(hsv, lower, upper)   
            mask = cv2.erode(mask, kernel, 1)
            return bool(np.mean(mask))
        
        def grassDay():
            dayLower = np.array([63, 127, 140]) 
            dayUpper = np.array([68, 165, 163])
            return threshold(dayLower, dayUpper)
        
        def grassNight():
            nightLower = np.array([65, 183, 51]) 
            nightUpper = np.array([68, 204, 77])
            return threshold(nightLower, nightUpper)
        
        if grassDay(): return False
        if grassNight(): return True
        return False

    def isNight():
        screen = mssScreenshotNP(0,0, mw, mh)
        # Convert the image from BGRA to HSV
        bgr = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

        #detect brightness
        if location == "spawn":
            return isNightSky(bgr)
        return isGrassNight(hsv) and isNightSky(bgr)

    if canDetectNight and isNight():
        print("night detected")

detectNight()