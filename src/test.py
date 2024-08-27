import pyautogui as pag
import modules.misc.appManager as appManager
from modules.screen.screenshot import mssScreenshot
import time
import cv2
from PIL import Image
import os
from modules.misc.imageManipulation import pillowToCv2

mw, mh = pag.size()
'''
appManager.openApp("roblox")
time.sleep(2)
mssScreenshot(mw*3/4, mh*2/3, mw//4,mh//3, True)
'''
def adjustImage(display_type, path, imageName):
        #get a list of all images and find the name of the one that matches
        images = os.listdir(path)
        for x in images:
            #images are named in the format itemname-width
            #width is the width of the monitor used to take the image
            name, res = x.split(".")[0].split("-",1)
            if name == imageName:
                img = Image.open(f"{path}/{x}")
                break
        #get original size of image
        width, height = img.size
        #calculate the scaling value 
        #retina has 2x more, built-in is 1x
        if display_type == res:
            scaling = 1
        elif display_type == "built-in": #screen is built-in but image is retina
            scaling = 2
        else: #screen is retina but image is built-in
            scaling = 0.5
        #resize image
        img = img.resize((int(width/scaling), int(height/scaling)))
        #convert to cv2
        return pillowToCv2(img)

target = adjustImage("built-in", "./images/blue", "died")
screen = cv2.imread("screen.png")
res = cv2.matchTemplate(screen, target, cv2.TM_CCOEFF_NORMED)
print(cv2.minMaxLoc(res))
