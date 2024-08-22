import cv2
import numpy as np
import time
# Define the color range for reset detection (in HSL color space)
resetLower = np.array([0, 102, 0])  # Lower bound of the color (H, L, S)
resetUpper = np.array([40, 255, 7])  # Upper bound of the color (H, L, S)
resetKernel = cv2.getStructuringElement(cv2.MORPH_RECT,(25,25))
screen = cv2.imread("screen3.png")

st = time.time()
# Convert the image from BGR to HLS color space
hsl = cv2.cvtColor(screen, cv2.COLOR_BGR2HLS)
# Create a mask for the color range
mask = cv2.inRange(hsl, resetLower, resetUpper)   
mask = cv2.erode(mask, resetKernel, 2)
#get contours. If contours exist, its correct
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if contours:
    print("yes")
print(time.time()-st)
imgRST = cv2.bitwise_and(screen, screen, mask = mask)
imgBGR = imgRST
cv2.imshow("src", screen)
cv2.imshow("result", imgBGR)
cv2.waitKey(0)
cv2.destroyAllWindows()