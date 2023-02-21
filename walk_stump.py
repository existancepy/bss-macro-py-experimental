
import pyautogui as pag
import time
import os
import tkinter
import loadsettings
import move
ws = loadsettings.load()["walkspeed"]
def ebutton(pagmode=0):
    r =  []
    savedata = loadRes()
    c = loadsettings.load()['ebthreshold']
    ww = savedata['ww']
    wh = savedata['wh']
    setdat = loadsettings.load()
    if setdat['ebdetect'] == "pyautogui" or pagmode:
        if setdat['display_type'] == "built-in retina display":
            r = pag.locateOnScreen("./images/retina/eb.png",confidence = 0.99,region=(ww//3,0,ww//3,wh//3))
        else:
            r = pag.locateOnScreen("./images/built-in/eb.png",confidence = 0.99,region=(ww//3,0,ww//3,wh//3))
    else:
        print("ebutton threshold: {}".format(c))
        r = imagesearch.find("eb.png",c,ww//3,0,ww//3,wh//3)
    if r:return r
    return

def apd(k):
    cmd = """
        osascript -e  'tell application "System Events" to key down "{}"'
    """.format(k)
    os.system(cmd)
def apu(k):
    cmd = """
        osascript -e  'tell application "System Events" to key up "{}"'
    """.format(k)
    os.system(cmd)


move.hold("s",5)
move.hold("d",6)
move.hold("w",9)
move.hold("d",2)
pag.keyDown("d")
time.sleep(0.1)
move.press("space")
time.sleep(0.15*28/ws)
pag.keyUp("d")
move.hold("w",7)
move.hold("d",4)
move.hold("s",0.5)
move.hold("a",0.1)
pag.keyDown("s")
time.sleep(0.1)
move.press("space")
time.sleep(0.15*28/ws)
pag.keyUp("s")
for _ in range(5):
    pag.keyDown("s")
    time.sleep(0.15)
    pag.keyUp("s")
    r = ebutton()
    if r:
        break
time.sleep(2.5)
move.press("e")
move.hold("w",4)
move.hold("d",3)
move.hold("s",0.6)


    
