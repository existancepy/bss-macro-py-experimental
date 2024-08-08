
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


self.keyboard.walk("s",5)
self.keyboard.walk("d",6)
self.keyboard.walk("w",9)
self.keyboard.walk("d",2)
self.keyboard.keyDown("d")
time.sleep(0.1)
self.keyboard.slowPress("space")
time.sleep(0.15*28/ws)
self.keyboard.keyUp("d")
self.keyboard.walk("w",7)
self.keyboard.walk("d",4)
self.keyboard.walk("s",0.5)
self.keyboard.walk("a",0.1)
self.keyboard.keyDown("s")
time.sleep(0.1)
self.keyboard.slowPress("space")
time.sleep(0.1*28/ws)
self.keyboard.keyUp("s")
time.sleep(2.5)
self.keyboard.slowPress("e")
self.keyboard.walk("w",4)
self.keyboard.walk("d",3)
self.keyboard.walk("s",0.6)


    
