import pyautogui as pag
import os
import tkinter
import move
import loadsettings
import time
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
cmd = """
        osascript -e  'activate application "Roblox"'
    """
os.system(cmd)
time.sleep(1)
pag.moveTo(350,100)
ww = savedata["ww"]
wh = savedata["wh"]
xo = ww//4
yo = wh-2
xt = xo//2
yt = 2
im = pag.screenshot(region = (xo,yo,xt,yt))
im.save('hive1.png')
cmd = """
        osascript -e  'activate application "Terminal"'
    """
os.system(cmd)

time.sleep(0.4)
    
    
