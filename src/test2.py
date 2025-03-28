import cv2
import numpy as np
import modules.screen.ocr as ocr
import pyautogui
import mss
import time
from rapidfuzz import fuzz
from PIL import Image

# Set up Tesseract path if needed (Windows users)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

TARGET_QUEST = "polar bear"  # Change this to your target quest title
CONFIDENCE_THRESHOLD = 80  # Adjust for fuzzy matching
SCROLL_AMOUNT = -500  # Adjust based on your screen's scroll sensitivity

# Function to detect and recognize quest text
def detect_text(img):
    # Preprocess the image
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply threshold
    thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(thresh, (5, 5), 0)

    kernel = np.ones((12, 12), np.uint8)  # Adjust kernel size to control merging strength
    dilated = cv2.dilate(blurred, kernel, iterations=1)

    # Find contours of the merged text chunks
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes around detected text
    out = []
    for contour in contours[::-1]:
        x, y, w, h = cv2.boundingRect(contour)
        textImg =  Image.fromarray(img_gray[y:y+h, x:x+w])
        temp = []
        for a in ocr.ocrRead(textImg):
            print(a)
            temp.append(a[1][0].strip().lower())
        out.append(' '.join(temp))
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)  # Green box

    print(out)
    # Show the processed image
    cv2.imshow("res", img)
    cv2.waitKey(0)

    return ""

# Function to check if quest is found
def quest_found(texts):
    for line in texts:
        if TARGET_QUEST in line:
            return True  # Quest found!
    return False  # Not found

# Main loop to scroll and search
screen_img = cv2.imread("quest.png")
detected_text = detect_text(screen_img)

print("Detected Text:", detected_text)  # Debugging output

if quest_found(detected_text):
    print("Quest found!")
else:
    print("Quest not found!")

