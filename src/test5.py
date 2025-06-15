import bitmap_matcher
from PIL import Image
import time
from modules.misc.appManager import getWindowSize
import cv2
import numpy as np
import mss

def screenshot(x,y,w,h):        
    with mss.mss() as sct:
        monitor = {"left": int(x), "top": int(y), "width": int(w), "height": int(h)}
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGBA", sct_img.size, sct_img.bgra, "raw", "BGRA")
        return img

x,y,w,h = getWindowSize("Roblox Roblox")
# Load both images
#bitmap_from_file = Image.open("huh.png").convert('RGBA')

bitmaps = []
for i in range(2,11):
    bitmaps.append(Image.open(f"counts/{i}.png").convert('RGBA'))

hasteBitmap = Image.new('RGBA', (10, 1), '#f0f0f0ff')
melodyBitmap = Image.new('RGBA', (3, 2), '#2b2b2bff')
#melodyBitmap = Image.open("melody.png").convert("RGBA")

def adjustBuffImage(self, path):
    img = Image.open(path).convert('RGBA')
    #get original size of image
    width, height = img.size
    #if its built-in, half the image
    scaling = 1 if self.isRetina else 2
    #resize image
    img = img.resize((int(width/scaling), int(height/scaling)))

bearMorphs = []
for i in range(5):
    bearMorphs.append(Image.open(f"bearmorph{i+1}-retina.png").convert('RGBA'))

start_time = time.time()
screen = Image.open(f"what2.png").convert('RGBA')
haste = 0
hasteX = None

x = 0
for _ in range(3):
    res = bitmap_matcher.find_bitmap_cython(screen, hasteBitmap, x=x, variance=1)
    if not res:
        break
    # x = res[0]
    # img = np.array(screen).copy()
    # img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)  # if image has alpha
    # x1, y1 = res
    # w = 10
    # h = 1
    # cv2.rectangle(img, (x1,y1), (x1+w, y1+h), (0,0,255), 1)
    # cv2.imshow("", img)
    # cv2.waitKey(0) 
    s = bitmap_matcher.find_bitmap_cython(screen, melodyBitmap, x=x+2, w=16*2, variance=2)
    if s:
        pass
        # img = np.array(screen).copy()
        # img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)  # if image has alpha
        # x1, y1 = s
        # w = 3
        # h = 2
        # cv2.rectangle(img, (x1,y1), (x1+w, y1+h), (0,0,255), 1)
        # cv2.imshow("", img)
        # cv2.waitKey(0) 
    if not s:
        hasteX = res[0]
        break
    x+= 40*2

if hasteX:
    for i, img in enumerate(bitmaps):
        res = bitmap_matcher.find_bitmap_cython(screen, img, x=hasteX, w=38*2, variance=2)
        if res:
            # img = np.array(screen).copy()
            # img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)  # if image has alpha
            # x1, y1 = res
            # w = 10
            # h = 30
            # cv2.rectangle(img, (x1,y1), (x1+w, y1+h), (0,0,255), 1)
            # cv2.imshow("", img)
            # cv2.waitKey(0) 
            haste = i+2
            break
    else:
        haste = 1

bearmorphSpeed = 0
for img in bearMorphs:
    res = bitmap_matcher.find_bitmap_cython(screen, img, variance=20)
    if res:
        bearmorphSpeed = 4
        print("bear")
        img = np.array(screen).copy()
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)  # if image has alpha
        x1, y1 = res
        w = 28
        h = 4
        cv2.rectangle(img, (x1,y1), (x1+w, y1+h), (0,0,255), 1)
        cv2.imshow("", img)
        cv2.waitKey(0) 
        break
    else:
        print("no bear")
    
end_time = time.time()
print(end_time-start_time)
print(haste)