import mss 
import numpy as np
from modules.screen.screenData import getScreenData
def getPixelColor(X1,Y1):
    if getScreenData()["display_type"] == "retina":
        X1/=2
        Y1/=2
    region = {'top': Y1, 'left': X1, 'width': 1, 'height': 1}
    
    with mss.mss() as sct:
        img = sct.grab(region)
        mss.tools.to_png(img.rgb, img.size, output='test.png')
        im = np.array(img)
        col = tuple(im[0,0])[:-1][::-1]
        return col