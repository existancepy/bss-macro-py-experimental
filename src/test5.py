from modules import bitmap_matcher
from PIL import Image
import time
from modules.misc.appManager import getWindowSize
import cv2
import numpy as np
import mss


# Load both images
#bitmap_from_file = Image.open("huh.png").convert('RGBA')


def adjustBuffImage(self, path):
    img = Image.open(path).convert('RGBA')
    #get original size of image
    width, height = img.size
    #if its built-in, half the image
    scaling = 1 if self.isRetina else 2
    #resize image
    img = img.resize((int(width/scaling), int(height/scaling)))


start_time = time.time()
screen = Image.open(f"what2.png").convert('RGBA')

img = Image.open(f"images/buffs/bearmorph5-retina.png").convert('RGBA')
res = bitmap_matcher.find_bitmap_cython(screen, img, variance=30)
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
else:
    print("no bear")
    
end_time = time.time()
print(end_time-start_time)