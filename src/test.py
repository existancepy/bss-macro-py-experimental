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

import cv2
import time
import math

# read game image
img = cv2.imread('screenshot2.png')

# read image template
template = cv2.imread('images/inventory/blueclayplanter-retina.png', cv2.IMREAD_UNCHANGED)
template = cv2.resize(template, (0, 0), fx = 0.5, fy = 0.5)
hh, ww = template.shape[:2]

# extract base image and alpha channel and make alpha 3 channels
base = template[:,:,0:3]
alpha = template[:,:,3]
alpha = cv2.merge([alpha,alpha,alpha])
cv2.imshow('result', alpha)
cv2.waitKey(0)
# do masked template matching and save correlation image
correlation = cv2.matchTemplate(img, base, cv2.TM_CCORR_NORMED, mask=alpha)

# set threshold and get all matches
threshold = 0.8

''' from:  https://stackoverflow.com/questions/61779288/how-to-template-match-a-simple-2d-shape-in-opencv/61780200#61780200 '''
# search for max score
result = img.copy()
max_val = 1
rad = int(math.sqrt(hh*hh+ww*ww)/4)

# find max value of correlation image
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(correlation)
print(max_val, max_loc)

if max_val > threshold:
    # draw match on copy of input
    cv2.rectangle(result, max_loc, (max_loc[0]+ww, max_loc[1]+hh), (0,0,255), 1)

    # save results
    cv2.imshow('result', result)
    cv2.waitKey(0)
else:
    print("No match found")


