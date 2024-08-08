
import pyautogui as pag
import time
import os
import tkinter
import loadsettings
import move
ws = loadsettings.load()["walkspeed"]

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


self.keyboard.slowPress(".")
self.keyboard.slowPress(".")
self.keyboard.slowPress(".")
self.keyboard.walk("w",15)
self.keyboard.slowPress(",")
self.keyboard.slowPress(",")
self.keyboard.slowPress(",")
move.apkey("space")
self.keyboard.keyDown("a")
time.sleep(12*28/ws)
self.keyboard.keyUp("a")
self.keyboard.walk("w",8)
self.keyboard.slowPress("space")
time.sleep(0.1)
self.keyboard.slowPress("space")
self.keyboard.keyDown("w")
time.sleep(4)
self.keyboard.slowPress(".")
time.sleep(0.5)
self.keyboard.slowPress('space')
self.keyboard.keyUp("w")
self.keyboard.walk("w",8)
self.keyboard.slowPress(",")
self.keyboard.walk("s",0.6)

    
