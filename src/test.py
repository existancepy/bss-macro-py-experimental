from paddleocr import PaddleOCR
from modules.screen.screenshot import mssScreenshot
import numpy as np
ocrP = PaddleOCR(lang='en', show_log = False, use_angle_cls=False)
def ocrPaddle(img):
    img = np.asarray(img) 
    result = ocrP.ocr(img, cls=False)[0]
    return result

img = mssScreenshot(0,0,500,500)
print(ocrPaddle(img))