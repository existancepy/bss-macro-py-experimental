import numpy as np
import time
import cv2
from modules.screen.screenshot import mssScreenshotNP
def isNightBrightness(hsv):
    hsv = hsv[int(hsv.shape[0]*2/5):hsv.shape[0]]
    vValues = np.sum(hsv[:, :, 2])
    area = hsv.shape[0] * hsv.shape[1]
    avg_brightness = vValues/area
    #threshold for night. It must be > 10 to deal with cases where the player is inside a fruit or stuck against a wall 
    print(avg_brightness)
    return 10 < avg_brightness < 80 

time.sleep(2)
screen = mssScreenshotNP(0,0, 1440, 900)
bgr = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
isNightBrightness(hsv)

