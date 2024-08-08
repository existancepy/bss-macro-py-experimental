
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


self.keyboard.walk("s",4.5)
time.sleep(0.5)
move.apkey("space")
self.keyboard.walk("a",6)
self.keyboard.walk("w",10)
self.keyboard.walk("d",12)
self.keyboard.walk("w",1.4)
self.keyboard.walk("s",0.6)

    
