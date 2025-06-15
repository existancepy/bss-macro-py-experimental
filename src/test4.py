from modules import bitmap_matcher
from PIL import Image
import time
from modules.misc.appManager import getWindowSize
import mss

def screenshot(x,y,w,h):        
    with mss.mss() as sct:
        monitor = {"left": int(x), "top": int(y), "width": int(w), "height": int(h)}
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGBA", sct_img.size, sct_img.bgra, "raw", "BGRA")
        return img

wx,wy,ww,wh = getWindowSize("Roblox Roblox")

bitmaps = []
for i in range(2,11):
    bitmaps.append(Image.open(f"counts/{i}.png").convert('RGBA'))

hasteBitmap = Image.new('RGBA', (10, 1), '#f0f0f0ff')
melodyBitmap = Image.new('RGBA', (3, 2), '#2b2b2bff')

bearMorphs = []
for i in range(5):
    bearMorphs.append(Image.open(f"./images/buffs/bearmorph{i+1}-retina.png").convert('RGBA'))

#similar to natro's implementation for haste detection
while True:
    start_time = time.time()
    screen = screenshot(wx,wy+52,ww,45)
    haste = 0
    hasteX = None

    x = 0
    #locate haste. It shares the same color as melody
    for _ in range(3):
        res = bitmap_matcher.find_bitmap_cython(screen, hasteBitmap, x=x, variance=1)
        if not res:
            break
        x = res[0]
        #can't find melody, so its haste
        if not bitmap_matcher.find_bitmap_cython(screen, melodyBitmap, x=x+2, w=16*2, variance=2):
            hasteX = res[0]
            break
        #melody, skip this buff
        x+= 40*2

    #haste found, get count
    if hasteX:
        for i, img in enumerate(bitmaps):
            res = bitmap_matcher.find_bitmap_cython(screen, img, x=hasteX, w=38*2, variance=3)
            if res:
                haste = i+2
                break
        else:
            haste = 1
    
    #search for bear morphs
    bearmorphSpeed = 0
    for img in bearMorphs:
        if bitmap_matcher.find_bitmap_cython(screen, img, variance=20):
            bearmorphSpeed = 4
            print("bear")
            break
    end_time = time.time()
    #print(end_time-start_time)
    print(haste)