from modules.misc.imageManipulation import pillowToCv2
from modules.screen.screenshot import mssScreenshot
from modules.misc.appManager import openApp
from modules.controls.keyboard import keyboard
import numpy as np
import cv2
import time
import pyautogui as pag

mw, mh = pag.size()
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(8,8))
#imgSRC is a cv2 img
def getSaturatorInImage(imgSRC):
    maxy, maxx = imgSRC.shape[:2]

    imgMSK = np.zeros((maxy, maxx, 3), np.uint8)
    imgHLS = cv2.cvtColor(imgSRC, cv2.COLOR_BGR2HLS)

    sLow = 250
    sHi = 255
    lLow = 120
    lHi = 200
    hLow = 170/2
    hHi = 220/2

    # Apply thresholds to each channel (H, L, S) using NumPy vectorized operations
    mask = (hLow <= imgHLS[:,:,0]) & (imgHLS[:,:,0] <= hHi) & \
        (lLow <= imgHLS[:,:,1]) & (imgHLS[:,:,1] <= lHi) & \
        (sLow <= imgHLS[:,:,2]) & (imgHLS[:,:,2] <= sHi)

    # Convert the mask to a 3-channel image
    imgMSK = np.zeros_like(imgSRC)
    imgMSK[mask] = [255, 255, 255]

    imgMSK = cv2.erode(imgMSK, kernel, 3)
    imgMSKGRAY = cv2.cvtColor(imgMSK, cv2.COLOR_BGR2GRAY)

    contours, _ = cv2.findContours(imgMSKGRAY, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours: return None
    # return the bounding with the largest area
    x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
    #display results
    '''
    cv2.rectangle(imgSRC, (x, y), (x+w, y+h), (0, 255, 0), 2)
    imgRST = cv2.bitwise_and(imgHLS, imgMSK)
    imgBGR = cv2.cvtColor(imgRST, cv2.COLOR_HLS2BGR)
    cv2.imshow("src", imgSRC)
    cv2.imshow("result", imgBGR)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    #get the center and return its coordinates
    return (x+w//2, y+h//2)

def getSaturatorLocation(isRetina):
    st = time.time()
    saturatorLocation = getSaturatorInImage(pillowToCv2(mssScreenshot(0,100, mw, mh-100)))
    if saturatorLocation is None: return None
    x,y = saturatorLocation
    if isRetina:
        x /= 2
        y /= 2
    y += 100
    print(time.time()-st)
    return (x,y)
    
def press(k,t):
    keyboard.keyDown(k, False)
    time.sleep(t)
    keyboard.keyUp(k, False)
    
def slowFieldDriftCompensation(isRetina, initialSaturatorLocation):
    winUp, winDown = mh/2.14, mh/1.88
    winLeft, winRight = mw/2.14, mw/1.88
    saturatorLocation = initialSaturatorLocation
    for _ in range(5):
        if saturatorLocation is None: break #cant find saturator
        x,y = saturatorLocation
        if x >= winLeft and x <= winRight and y >= winUp and y <= winDown: 
            break
        if x < winLeft:
            press("a",0.3)
        elif x > winRight:
            press("d",0.3)
        if y < winUp:
            press("w",0.3)
        elif y > winDown:
           press("s",0.3)

        saturatorLocation = getSaturatorLocation(isRetina)



#natro's field drift compensation
#works well with fast detection times (<0.2s)
def fastFieldDriftCompensation(isRetina, initialSaturatorLocation):
    
    winUp, winDown = mh/2.14, mh/1.88
    winLeft, winRight = mw/2.14, mw/1.88
    i = 0
    hmove, vmove = 1, 1
    if initialSaturatorLocation:
        x,y = initialSaturatorLocation

        #move towards saturator
        if x >= winLeft and x <= winRight and y >= winUp and y <= winDown: 
            return
        if x < winLeft:
            keyboard.keyDown("a", False)
            hmove = "a"
        elif x > winRight:
            keyboard.keyDown("d", False)
            hmove = "d"
        if y < winUp:
            keyboard.keyDown("w", False)
            vmove = "w"
        elif y > winDown:
            keyboard.keyDown("s", False)
            vmove = "s"
        
        while hmove or vmove:
            #check if reached saturator
            if (hmove == "a" and x >= winLeft) or (hmove == "d" and x <= winRight):
                keyboard.keyUp(hmove, False)
                hmove = ""
                   
            if (vmove == "w" and y >= winUp) or (vmove == "s" and y <= winDown):
                keyboard.keyUp(vmove, False)
                vmove = ""
            
            time.sleep(0.02)
            #too many iterations, just give up
            if i >= 100:
                keyboard.releaseMovement()
                break
            #update saturator location
            saturatorLocation = getSaturatorLocation(isRetina)
            if saturatorLocation is not None:
                x,y = saturatorLocation

            else: #cant find saturator, pause
                keyboard.releaseMovement()
                #try to find saturator
                print("a")
                for _ in range(20):
                    time.sleep(0.02)
                    saturatorLocation = getSaturatorLocation(isRetina)
                    #saturator found
                    if saturatorLocation:
                        #move towards saturator
                        if hmove:
                            keyboard.keyDown(hmove)
                        if vmove:
                            keyboard.keyDown(vmove)
                        x,y = saturatorLocation
                        break
                else: #still cant find it, give up
                    break
            i += 1
            
def fieldDriftCompensation(isRetina):
    #calculate how fast it takes to get the saturator and determine if the fast or slow version should be used
    st = time.time()
    saturatorLocation = getSaturatorLocation(isRetina)
    timing = time.time()-st
    if timing > 0.25:
        slowFieldDriftCompensation(isRetina, saturatorLocation)
    else:
        fastFieldDriftCompensation(isRetina, saturatorLocation)
        
openApp("roblox")
time.sleep(1)
fieldDriftCompensation(False)
