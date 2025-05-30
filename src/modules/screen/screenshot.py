import mss
from PIL import Image
import mss.tools
import time
import pyautogui as pag
import numpy as np
import cv2
import time
import os
import tempfile
import subprocess
import Quartz.CoreGraphics as CG

mw, mh = pag.size()
def pillowGrab(x,y,w,h):
    fh, filepath = tempfile.mkstemp(".png")
    os.close(fh)
    args = ["screencapture"]
    subprocess.call(args + ["-x", filepath])
    im = Image.open(filepath)
    im.load()
    os.unlink(filepath)
    bbox = (x, y, x + w, y + h)
    im_cropped = im.crop(bbox)
    im.close()
    return im_cropped

def cgGrab(region=None):
    # Set up the screen capture rectangle
    if region:
        left, top, width, height = region
    else:
        main_display_id = CG.CGMainDisplayID()
        width = CG.CGDisplayPixelsWide(main_display_id)
        height = CG.CGDisplayPixelsHigh(main_display_id)
        left, top = 0, 0

    rect = CG.CGRectMake(left, top, width, height)

    # Capture the screen region as an image
    image_ref = CG.CGWindowListCreateImage(
        rect,
        CG.kCGWindowListOptionOnScreenOnly,
        CG.kCGNullWindowID,
        CG.kCGWindowImageDefault
    )

    # Get image width/height and raw pixel data
    width = CG.CGImageGetWidth(image_ref)
    height = CG.CGImageGetHeight(image_ref)
    bytes_per_row = CG.CGImageGetBytesPerRow(image_ref)
    data_provider = CG.CGImageGetDataProvider(image_ref)
    data = CG.CGDataProviderCopyData(data_provider)

    # Convert to NumPy array
    img = np.frombuffer(data, dtype=np.uint8).reshape((height, bytes_per_row // 4, 4))
    img = img[:, :width, :]  # Trim padding if needed

    # Convert to PIL Image (in BGRA format)
    return img
 
#returns an NP array, useful for cv2
def mssScreenshotNP(x,y,w,h, save = False):
    return cgGrab((x,y,w,h))
    # screen = pillowGrab(int(x*2),int(y*2),int(w*2),int(h*2))
    # screen = np.array(screen)
    # screen_bgra = cv2.cvtColor(screen, cv2.COLOR_RGB2BGRA)
    # return screen_bgra

    # with mss.mss() as sct:
    #     # The screen part to capture
    #     monitor = {"left": int(x), "top": int(y), "width": int(w), "height": int(h)}
    #     # Grab the data and convert to opencv img
    #     sct_img = sct.grab(monitor)
    #     if save: mss.tools.to_png(sct_img.rgb, sct_img.size, output=f"screen-{time.time()}.png")
    #     return np.array(sct_img)


def mssScreenshot(x=0,y=0,w=mw,h=mh, save = False):
    img = cgGrab((x,y,w,h))
    img = img[:, :, [2, 1, 0]]
    img = Image.fromarray(img, 'RGB')
    return img

    #return pillowGrab(int(x*2),int(y*2),int(w*2),int(h*2))

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
