import mss
from PIL import Image
import mss.tools

def mssScreenshot(x,y,w,h):
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {"left": int(x), "top": int(y), "width": int(w), "height": int(h)}
        # Grab the data and convert to pillow img
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        return img

def screenshotScreen(path):
    with mss.mss() as sct:
        sct.shot(output=path)
