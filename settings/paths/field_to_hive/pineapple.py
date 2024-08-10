
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


self.keyboard.walk("s",3)
self.keyboard.walk("w",0.15)
self.keyboard.walk("a",6)
self.keyboard.walk("w",10)
self.keyboard.walk("d",4)
self.keyboard.walk("s",0.5)
self.keyboard.walk("a",0.1)
self.keyboard.keyDown("s")
time.sleep(0.1)
self.keyboard.slowPress("space")
time.sleep(0.15*28/ws)
self.keyboard.keyUp("s")
self.keyboard.walk("s",0.05)
time.sleep(2.5)
self.keyboard.slowPress("e")
self.keyboard.walk("w",4)
self.keyboard.walk("d",3)
self.keyboard.walk("s",0.5)

    
