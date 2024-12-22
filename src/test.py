'''
import cv2
from PIL import Image

# Load the image
image_path = "test.png"
image = cv2.imread(image_path)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply a threshold to binarize the image (black and white)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Remove noise using a morphological operation (optional for cleaner text)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

cv2.imshow("final", morphed)
cv2.waitKey(0)
'''
'''
import pylivestream.api as liveStream

liveStream.stream_screen("./pylivestream.json", websites=["youtube"], assume_yes = True)
'''

import cv2
import numpy as np
import pyautogui as pag
from modules.screen.screenshot import mssScreenshotNP
import time
mw, mh = pag.size()

def findColorObjectHSL(img, hslRange, kernel=None, mode="point", best=1, draw=False):
    """
    Quickly find objects of a specific color in the HSL range.

    Args:
        img (numpy.ndarray): Input image in BGR format.
        hslRange (list): HSL range [(H_min, S_min, L_min), (H_max, S_max, L_max)].
        kernel (numpy.ndarray): Kernel for erosion (optional).
        mode (str): "point" to return center of bounding box, "box" to return bounding boxes.
        best (int): Number of top contours to return (default 1).
        draw (bool): Whether to draw bounding boxes on the image.

    Returns:
        tuple or list: Coordinates of the center or bounding boxes.
    """
    # Convert HSL range to OpenCV's HLS format
    hLow, sLow, lLow = hslRange[0][0] / 2, hslRange[0][1] / 100 * 255, hslRange[0][2] / 100 * 255
    hHigh, sHigh, lHigh = hslRange[1][0] / 2, hslRange[1][1] / 100 * 255, hslRange[1][2] / 100 * 255

    # Fast conversion to HLS and thresholding
    binary_mask = cv2.inRange(
        cv2.cvtColor(img, cv2.COLOR_BGR2HLS),
        np.array([hLow, lLow, sLow], dtype=np.uint8),
        np.array([hHigh, lHigh, sHigh], dtype=np.uint8)
    )

    # Optional erosion
    if kernel is not None:
        binary_mask = cv2.erode(binary_mask, kernel, iterations=1)

    # Find contours directly
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None

    # Sort contours once if best > 1
    if best > 1:
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:best]

    results = []
    for contour in (contours if best > 1 else [max(contours, key=cv2.contourArea)]):
        x, y, w, h = cv2.boundingRect(contour)
        results.append((x + w // 2, y + h // 2) if mode == "point" else (x, y, w, h))
        if draw:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if draw:
        cv2.imshow("Result", img)
        cv2.waitKey(0)

    return results if best > 1 else results[0]

time.sleep(2)
st = time.time()
screen = mssScreenshotNP(0, 100, mw/2, mh-200)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
res = findColorObjectHSL(screen, [(270, 25, 20), (310, 80, 80)], kernel=kernel, best=1, draw=True)
print(res)