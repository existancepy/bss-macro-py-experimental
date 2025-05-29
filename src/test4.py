import cv2
from modules.screen.screenshot import mssScreenshot, mssScreenshotNP
import numpy as np
import imagehash
import time
import pyautogui as pag
from modules.misc.imageManipulation import adjustImage
from modules.screen.imageSearch import locateImageOnScreen

mw, mh = pag.size()

yesImg = adjustImage("./images/menu", "yes", "retina")
locateImageOnScreen(yesImg,.mw/3.2,mh/2.3,mw/2.5,mh/3.4, threshold)
