from PIL import ImageGrab
import time
from PIL import Image
import Quartz.CoreGraphics as CG
from PIL import Image
import numpy as np
import mss

def grab(region=None):
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
    return Image.fromarray(img, 'RGBA')  # Can use 'BGRA' if needed

st = time.time()
ImageGrab.grab()
print(time.time()-st)

st = time.time()
img = grab()
print(time.time()-st)

st = time.time()
with mss.mss() as sct:
    # The screen part to capture
    monitor = {"left": int(0), "top": int(0), "width": int(1440), "height": int(900)}
    # Grab the data and convert to opencv img
    sct_img = sct.grab(monitor)
print(time.time()-st)