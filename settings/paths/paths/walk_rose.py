
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
self.keyboard.walk("w",6)
self.keyboard.walk("a",5)
self.keyboard.slowPress(",")
self.keyboard.walk("a",7)
self.keyboard.slowPress(".")
self.keyboard.walk("d",6)
self.keyboard.walk("s",3)
self.keyboard.walk("a",8)
self.keyboard.slowPress(",")
self.keyboard.slowPress(",")
self.keyboard.slowPress(",")
self.keyboard.walk("w",16)
self.keyboard.slowPress(".")
self.keyboard.walk("s",0.5)
self.keyboard.walk("d",4)
self.keyboard.walk("w",1.4)
self.keyboard.walk("s",0.5)
