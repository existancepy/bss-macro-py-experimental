import cv2
import numpy as np
from modules.submacros.hourlyReport import getBuffQuantityFromImg
# Load images
screen = cv2.imread("he.png")
hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)

# Define green range
lower = np.array([50, 180, 180])
upper = np.array([80, 255, 255])
mask = cv2.inRange(hsv, lower, upper)

out = 0
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

retina = True
buffSize = 76 if retina else 39
# Loop through contours and get bounding boxes
for cnt in contours:
    rect = cv2.boundingRect(cnt)
    x, y, w, h = rect

    #filter area to avoid noise
    if buffSize-5 < w < buffSize+5:
        print(f"Buff detected at: x={x}, y={y}, width={w}, height={h}")
        # Draw rectangle to visualize
        #crop out
        y = min(0, y+buffSize-h)
        cv2.rectangle(screen, (x, y), (x + w, y + buffSize), (0, 100, 255), 2)
        buffImg = screen[y:y+buffSize, x:x+buffSize]
        out = getBuffQuantityFromImg(buffImg, True)

print(out)
cv2.imshow("Detected Buffs", screen)
cv2.waitKey(0)
cv2.destroyAllWindows()