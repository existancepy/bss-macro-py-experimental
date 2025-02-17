import numpy as np
import time
import cv2
from modules.screen.screenshot import mssScreenshotNP
from modules.screen.imageSearch import findColorObjectHSL, findColorObjectRGB

bgr = cv2.imread("night.png")

dayColors = [
    #[(47, 117, 57), cv2.getStructuringElement(cv2.MORPH_RECT, (6, 6))], #ground
    [(46, 117, 58), cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))], #dande
    [(60, 156, 74), cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))], #stump
    [(38, 114, 51), cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))], #pa
    [(66, 123, 40), cv2.getStructuringElement(cv2.MORPH_RECT, (6, 6))], #clov
    [(32, 211, 22), cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))], #ant
]

nightColors = [
    [(23, 72, 30), cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))], #a
    [(17, 71, 28), cv2.getStructuringElement(cv2.MORPH_RECT, (6, 6))], #dande
]

bgr = bgr[0:bgr.shape[0]-200]
#detect night 5 times in a row
for _ in range(5):
    #detect day
    for color, kernel in dayColors:
        if findColorObjectRGB(bgr, color, variance=6, kernel=kernel, mode="box"):
            print("No")
    #day not found, detect Night
    else:
        for color, kernel in nightColors:
            if findColorObjectRGB(bgr, color, variance=6, kernel=kernel, mode="box"):
                break
        else: #neither day nor night detected
            print("No")
    
print("Yes")
