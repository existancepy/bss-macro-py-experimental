
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

start = time.time()
move.press(",")
move.press("e")
time.sleep(0.95)
pag.keyDown("w")
move.press("space")
move.press("space")
time.sleep(10)
pag.keyUp("w")
move.press("space")
time.sleep(0.8)
move.press(",")
move.hold("w",1)
move.press(",")
move.press(",")
pag.keyDown("w")
sleep(2)
move.press("space")
sleep(0.8)
pag.keyUp("w")
move.press(",")
move.press(",")
