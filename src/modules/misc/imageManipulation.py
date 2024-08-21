import numpy as np
import cv2

#accept a pillow image and return a cv2 one
def pillowToCv2(img):
    return cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)