#hsv(128.57, 58.33%, 61.18%)
#hsv(128.48, 58.6%, 61.57%)
#hsv(132.63, 52.78%, 56.47%)
#hsv(129.68, 60.78%, 60%)
#hsv(129.28, 63.4%, 60%)
#hsv(131.21, 57.96%, 61.57%)

#hsv(132.22, 76.06%, 27.84%)
#hsv(131.25, 77.42%, 24.31%)
#hsv(134.4, 75.76%, 25.88%)
import cv2
import numpy as np

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
    if grassNight: return True
    return False

screen = cv2.imread("day.png")
hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
print(isGrassNight(hsv))