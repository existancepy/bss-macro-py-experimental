import mss
from PIL import Image
import mss.tools
import time
import pyautogui as pag
import numpy as np
import cv2
import time

mw, mh = pag.size()
#returns an NP array, useful for cv2
def mssScreenshotNP(x,y,w,h, save = False):
    screen = pag.screenshot(region=(int(x*2),int(y*2),int(w*2),int(h*2)))
    screen = np.array(screen)
    screen_bgra = cv2.cvtColor(screen, cv2.COLOR_RGB2BGRA)
    return screen_bgra
    # with mss.mss() as sct:
    #     # The screen part to capture
    #     monitor = {"left": int(x), "top": int(y), "width": int(w), "height": int(h)}
    #     # Grab the data and convert to opencv img
    #     sct_img = sct.grab(monitor)
    #     if save: mss.tools.to_png(sct_img.rgb, sct_img.size, output=f"screen-{time.time()}.png")
    #     return np.array(sct_img)


def mssScreenshot(x=0,y=0,w=mw,h=mh, save = False):
    return pag.screenshot(region=(int(x*2),int(y*2),int(w*2),int(h*2)))
    # st = time.time()
    # print(f"x:{x}, y:{y}, w: {w}, h:{h}")
    # with mss.mss() as sct:
    #     # The screen part to capture
    #     monitor = {"left": int(x), "top": int(y), "width": int(w), "height": int(h)}
    #     # Grab the data and convert to pillow img
    #     sct_img = sct.grab(monitor)
    #     print(f"grabbed monitor: {time.time()-st}")
    #     img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
    #     print(f"converted image: {time.time()-st}")
    #     if save: mss.tools.to_png(sct_img.rgb, sct_img.size, output=f"screen-{time.time()}.png")
    #     return img

def screenshotScreen(path, region = None):
    with mss.mss() as sct:
        if region is None:
            sct.shot(output=path)
        else:
            monitor = {"left": int(region[0]), "top": int(region[1]), "width": int(region[2]), "height": int(region[3])}
            sct_img = sct.grab(monitor)
            # Save to the picture file
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=path)
