
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


self.keyboard.walk("s",7)
self.keyboard.walk("d",6)
self.keyboard.walk("w",11)
self.keyboard.walk("s",0.15)
self.keyboard.walk("d",0.35)
self.keyboard.walk("w",4)
self.keyboard.walk("d",3)
self.keyboard.walk("s",0.6)

    
