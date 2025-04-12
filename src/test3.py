import cv2
import modules.screen.ocr as ocr
from PIL import Image
import numpy as np

objectives = ["gather_blue flower", "kill_30_ladybug"]

def convertCyrillic(original):
    out = ""
    for x in original:
        if x in cyrillicToLatin:
            x = cyrillicToLatin[x]
        out += x
    return out

cyrillicToLatin = {
    'А': 'A', 'В': 'B', 'Е': 'E', 'К': 'K', 'М': 'M', 'Н': 'H',
    'О': 'O', 'Р': 'P', 'С': 'C', 'Т': 'T', 'У': 'Y', 'Х': 'X',
    'а': 'a', 'в': 'B', 'е': 'e', 'к': 'k', 'м': 'm', 'н': 'h',
    'о': 'o', 'р': 'p', 'с': 'c', 'т': 't', 'у': 'y', 'х': 'x'
}

# Load image in grayscale and also in color for drawing
screen_gray = cv2.imread("quest.png", 0)
screen_color = cv2.imread("quest.png")

# Preprocess the image
img = cv2.threshold(screen_gray, 150, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
img = cv2.GaussianBlur(img, (5, 5), 0)

# Dilate the image to merge text into chunks
kernelSize = 10
kernel = np.ones((kernelSize, kernelSize), np.uint8) 
img = cv2.dilate(img, kernel, iterations=1)
cv2.imshow("sussy", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
# Find contours
contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
completedObjectives = []
incompleteObjectives = []

min_area = 1000       # Too small = noise
max_area = 50000      # Too big = background or large UI elements
max_height = 80       # Cap height to filter out title bar

count = 0
# Process and draw bounding boxes
for contour in contours[::-1]:
    x, y, w, h = cv2.boundingRect(contour)
    area = w*h
    if area < min_area or area > max_area or h > max_height:
        cv2.rectangle(screen_color, (x, y), (x+w, y+h), (0, 255, 255), 1)  # Yellow = skipped
        continue

    textImg = Image.fromarray(screen_gray[y:y+h, x:x+w])
    
    textChunk = []
    for line in ocr.ocrRead(textImg):
        textChunk.append(convertCyrillic(line[1][0].strip().lower()))
    textChunk = ''.join(textChunk)
    print(textChunk)

    if "complete" in textChunk:
        completedObjectives.append(objectives[count])
        color = (0, 255, 0)  # Green
    else:
        incompleteObjectives.append(objectives[count])
        color = (0, 0, 255)  # Red

    # Draw rectangle on the color image
    cv2.rectangle(screen_color, (x, y), (x+w, y+h), color, 2)
    cv2.putText(screen_color, objectives[count], (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    count += 1

# Show and/or save the result
cv2.imshow("Detected Objectives", screen_color)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Completed:", completedObjectives)
print("Incomplete:", incompleteObjectives)
