
import pyautogui as pag
import time
import os
import tkinter
import loadsettings
import move
from delay import sleep

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
self.keyboard.slowPress("e")
sleep(0.08)
self.keyboard.keyDown("w")
sleep(0.73)
self.keyboard.slowPress("space")
self.keyboard.slowPress("space")
sleep(0.7)
self.keyboard.slowPress("space")
sleep(1)
self.keyboard.walk("w",3)
self.keyboard.walk("a",1)
self.keyboard.walk("d",0.3)
self.keyboard.walk("s",0.3)

    
