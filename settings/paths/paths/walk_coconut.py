
import pyautogui as pag
import time
import os
import tkinter
import loadsettings
import move


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
    
self.keyboard.walk("d",4)
self.keyboard.walk("s",3)
self.keyboard.keyDown("s")
self.keyboard.slowPress('space')
time.sleep(0.2)
self.keyboard.keyUp("s")
self.keyboard.walk("s",5)
self.keyboard.walk("a",5)
self.keyboard.walk("w",4)
self.keyboard.walk("s",0.2)
self.keyboard.walk("d",7)
self.keyboard.walk("w",1)
self.keyboard.walk("s",0.6)





    
