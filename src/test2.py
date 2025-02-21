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
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    img = cv2.GaussianBlur(img, (5, 5), 0)
    cv2.imshow("res", img)
    cv2.waitKey(0)
    
    # Extract text
    img = Image.fromarray(img)
    texts = []
    for x in ocr.ocrRead(img):
        text = x[1][0].strip().lower()
        if "complete" in text:
            texts[-1] += " " + text
        else:
            texts.append(text) 

    return texts

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

