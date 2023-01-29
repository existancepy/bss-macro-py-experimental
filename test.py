
import pyautogui as pag
import time
import os
import tkinter
import move
import sys
import cv2
from PIL import ImageGrab
import numpy as np
import imagesearch
import loadsettings

import tkinter as tk
import tty
from tkinter import ttk
import backpack
from webhook import webhook
import webbrowser
import reset


cmd = """
osascript -e 'activate application "Roblox"' 
"""
os.system(cmd)

time.sleep(1)
savedata = {}
def loadSave():
    with open('save.txt') as f:
        lines = f.read().split("\n")
    f.close()
    for s in lines:
        l = s.replace(" ","").split(":")
        if l[1].isdigit():
            l[1] = int(l[1])
        savedata[l[0]] = l[1]
loadSave()
setdat = loadsettings.load()
ww = savedata["ww"]
wh = savedata["wh"]
ms = pag.size()
mw = ms[0]
mh = ms[1]


def displayPlanterName(planter):
    if planter == "redclay":
        return "Red Clay Planter"
    elif planter == "blueclay":
        return "Blue Clay Planter"
    elif planter  == "heattreated":
        return "Heat-Treated Planter"
    elif planter == "plenty":
        return "The Planter of Plenty"
    return "{} Planter".format(planter.title())
    
def placePlanter(planter):
    pag.moveTo(315,224)
    scroll_start = time.time()
    while True:
        pag.scroll(100000)
        if time.time() - scroll_start > 3:
            break
    if not imagesearch.find("sprinklermenu.png".format(planter),0.6,0,wh//10,ww//3,wh):
        pag.moveTo(27,102)
        pag.click()
    pag.moveTo(315,224)
    time.sleep(1)
    setdat = loadsettings.load()
    scroll_start = time.time()
    while True:
        pag.scroll(-100000)
        if time.time() - scroll_start > 3:
            break
    planter_find_start = time.time()
    while True:
        pag.scroll(2400)
        if time.time()-planter_find_start > 30:
            webhook("",'Cant Find: {}'.format(displayPlanterName(planter)),"dark brown")
            break
        if imagesearch.find("{}planter.png".format(planter),0.6,0,wh//10,ww//3,wh):
            time.sleep(0.5)
            r = imagesearch.find("{}planter.png".format(planter),0.6,0,0,ww,wh)
            webhook("",'Found: {}'.format(displayPlanterName(planter)),"dark brown")
            trows,tcols = cv2.imread('./images/retina/{}planter.png'.format(planter)).shape[:2]
            urows,ucols = cv2.imread('./images/retina/yes.png').shape[:2]
            if setdat['display_type'] == "built-in retina display":
                print(r[1],r[2])
                
                pag.moveTo(r[1]//2+trows//4,r[2]//2+tcols//4)
                time.sleep(0.5)
                pag.dragTo(ww//4, wh//4,0.7, button='left')
                time.sleep(0.5)
                a = imagesearch.find("yes.png",0.5,0,0,ww,wh)
                if a:
                    pag.moveTo(a[1]//2+urows//4,a[2]//2+ucols//4)
                    pag.click()
                else:
                    pag.moveTo(ww//4-70,wh//3.2)
                    pag.click()
            else:
                pag.moveTo(r[1]+trows//2,r[2]+tcols//2)
                pag.dragTo(ww//2, wh//2,0.8, button='left')
                pag.moveTo(ww//4-70,wh//3.2)
                time.sleep(0.5)
                a = imagesearch.find("yes.png",0.5,0,0,ww,wh)
                if a:
                    pag.moveTo(a[1]+urows//2,a[2]+ucols//2)
                    pag.click()
                else:
                    pag.moveTo(ww//2-50,wh//1.6)
                    pag.click()

            break
def goToPlanter(field,place=0):
    exec(open("field_{}.py".format(field)).read())
    if field == "pine tree":
        move.hold("d",3)
        move.hold("s",4)
        if place: move.hold("w",0.07)
    elif field == "pumpkin":
        move.hold("s",3)
        move.press(",")
        move.press(",")
        move.hold("w",4)
        if place: move.hold("s",0.07)
    elif field  == "strawberry":
        move.hold("d",3)
        move.hold("s",4)
    elif field == "bamboo":
        move.hold("s",3)
        move.press(",")
        move.press(",")
        move.hold("w",4)
        if place: move.hold("s",0.07)
    elif field  == "pineapple:
        move.hold("d",3)
        move.hold("s",4)
    elif field == "mushroom":
        move.hold("s",3)
        move.press(",")
        move.press(",")
        move.hold("w",4)
        if place: move.hold("s",0.07)
    elif field == "coconut":
        move.hold("d",5)
        move.hold("s")
        
reset.reset()    
goToPlanter()
placePlanter('tacky')

'''



savedata = {}
def loadSave():
    with open('save.txt') as f:
        lines = f.read().split("\n")
    f.close()
    for s in lines:
        l = s.replace(" ","").split(":")
        if l[1].isdigit():
            l[1] = int(l[1])
        savedata[l[0]] = l[1]
        
def savesettings(dictionary):
    templist = []
    for i in dictionary:
        templist.append("\n{}:{}".format(i,dictionary[i]))
        print(templist)
    with open('settings.txt', "w") as f:
        f.writelines(templist)
    f.close()

size = 1
width = 1


def loadtimings():
    tempdict = {}
    with open('timings.txt') as f:
        lines = f.read().split("\n")
    f.close()
    for s in lines:
        l = s.replace(" ","").split(":")
        if l[1].isdigit():
            l[1] = int(l[1])
        tempdict[l[0]] = l[1]
    return tempdict

def savetimings(m):
    tempdict = loadtimings()
    print(tempdict)
    tempdict[m] = time.time()
    templist = []
    
    for i in tempdict:
        templist.append("\n{}:{}".format(i,tempdict[i]))
    print(templist)
    with open('timings.txt','w') as f:
        f.writelines(templist)
    f.close()
setdat = loadsettings.load()
def canon():
    #Move to canon:
    webhook("","Moving to canon","dark brown")
    move.hold("w",2)
    move.hold("d",0.9*(setdat["hive_number"])+1)
    pag.keyDown("d")
    time.sleep(0.5)
    move.press("space")
    time.sleep(0.2)
    st = time.perf_counter()
    r = ""
    pag.keyUp("d")
    while True:
        pag.keyDown("d")
        time.sleep(0.15)
        pag.keyUp("d")
        r = pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2))
        if r:
            webhook("","Canon found","dark brown")
            return
        if time.perf_counter()  - st > 10/28*setdat["walkspeed"]:
            webhook("","Cannon not found, resetting","dark brown")
            break
        
    reset.reset()   
    canon()
def rawreset():
    pag.press('esc')
    time.sleep(0.1)
    pag.press('r')
    time.sleep(0.2)
    pag.press('enter')
    time.sleep(8) 
def updateHive(h):
    webhook("","Found Hive: {}".format(h),"bright  green")
    settings = loadsettings.save()['hive_number',h]
def rejoin():
    cmd = """
        osascript -e 'tell application "Roblox" to quit' 
        """
    os.system(cmd)
    webhook("","Rejoining","dark brown")
    if setdat["private_server_link"]:
        webbrowser.open(setdat['private_server_link'])
    else:
        webbrowser.open('https://www.roblox.com/games/1537690962/Bee-Swarm-Simulator')
        time.sleep(5)
        _,x,y = imagesearch.find('playbutton.png',0.8)
        webhook("","Play Button Found","dark brown")
        if setdat['display_type'] == "built-in retina display":
            pag.click(x//2, y//2)
        else:
            pag.click(x, y)
    move.hold("w",5)
    move.hold("s",0.55)
    foundHive = 0
    webhook("","Finding Hive", "dark brown")
    if setdat['hive_number'] == 3:
        if pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2)):
            move.press('e')
            foundHive = 1
    elif setdat['hive_number'] == 2:
        move.hold('d',1.2)
        if pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2)):
                move.press('e')
                foundHive = 1
    elif setdat['hive_number'] == 1:
        move.hold('d',2.3)
        if pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2)):
            move.press('e')
            foundHive = 1
    elif setdat['hive_number'] == 4:
        move.hold('a',1.1)
        if pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2)):
                move.press('e')
                foundHive = 1
    elif setdat['hive_number'] == 5:
        move.hold('a',2.3)
        if pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2)):
            move.press('e')
            foundHive = 1
    else:
        move.hold('a',3.3)
        if pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2)):
                move.press('e')
                foundHive = 1
    while True:   
        if not foundHive:
            webhook("","Hive already claimed, finding new hive","dark brown")
            rawreset()
            move.hold("w",5)
            move.hold("s",0.55)
            if pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2)):
                move.press('e')
                foundHive = 1
                updateHive(3)
                break
            move.hold('d',1.2)
            if pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2)):
                move.press('e')
                foundHive = 1
                updateHive(2)
                break
            move.hold('d',1.1)
            if pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2)):
                move.press('e')
                foundHive = 1
                updateHive(1)
                break
            rawreset()
            move.hold("w",5)
            move.hold("s",0.55)
            move.hold('a',1.1)
            if pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2)):
                move.press('e')
                foundHive = 1
                updateHive(4)
                break
            move.hold('a',1.1)
            if pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2)):
                move.press('e')
                foundHive = 1
                updateHive(5)
                break
            move.hold('a',1)
            if pag.locateOnScreen("./images/eb.png",region=(0,0,ww,wh//2)):
                move.press('e')
                foundHive = 1
                updateHive(6)
                break
            break
        else: break
    if not foundHive:
        rawreset()
        move.hold("w",5)
        move.hold("s",0.55)
        move.hold('d',4)
        starttime = time.time()
        pag.keyDown("d")
        while time.time()-starttime < 10:
            key.press("e")
        pag.keyUp("d")
        updateHive(6)
    convert()
'''



'''



r = pag.locateCenterOnScreen("./images/saturator.png",confidence=0.97)
if r:
    print(r)
    pag.moveTo(r[0]//2,r[1]//2)


winup = wh / 2.14
windown = wh / 1.88
winleft = ww / 2.14
winright = wh / 1.88

method = cv2.TM_SQDIFF_NORMED
screen = np.array(ImageGrab.grab())
screen = cv2.cvtColor(src=screen, code=cv2.COLOR_BGR2RGB)

small_image = cv2.imread('./images/saturator.png')
large_image = screen
result = cv2.matchTemplate(small_image, large_image, method)
mn,_,mnLoc,_ = cv2.minMaxLoc(result)
MPx,MPy = mnLoc
print(MPx,MPy)
pag.moveTo(MPx//2,MPy//2)
# Step 2: Get the size of the template. This is the same size as the match.
trows,tcols = small_image.shape[:2]

# Step 3: Draw the rectangle on large_image
cv2.rectangle(large_image, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,255),2)

# Display the original image with the rectangle around the match.
cv2.imshow('output',large_image)

# The image is only displayed if we call this
cv2.waitKey(0)

while True:
    r = imagesearch.find("saturator.png",0.9,0,0,ww,wh,1)

    if abs(x-winleft) < 50 and abs(y-winup) < 50:
        break
    elif mn < 0.007:
        if x < winleft:
            move.hold("a",0.1)
            print("a")
        elif x > winright:
            move.hold("d",0.1)
            print("d")

        if y < winup:
            move.hold("w",0.1)
            print("w")
        elif y > windown:
            move.hold("s",0.1)
            print("s")
'''





