import pyautogui as pag
import os
import tkinter
import move
import loadsettings
import time
import Quartz
setdat = loadsettings.load()
sizeword = setdat["gather_size"]
width = setdat["gather_width"]
size = 0
if sizeword.lower() == "s":
    size = 1
elif sizeword.lower() == "m":
    size = 1.5
else:
    size = 2


move.hold("s",0.5*size)
move.hold("a",abs(0.17*width*2))
for _ in range(width):
    move.hold("w",0.5*size)
    move.hold("d",0.17)
    move.hold("s",0.5*size)
    move.hold("d",0.17)
move.hold("w",0.5*size)
move.hold("a",abs(0.17*width*2))
for _ in range(width):
    move.hold("s",0.5*size)
    move.hold("d",0.17)
    move.hold("w",0.5*size)
    move.hold("d",0.17)




        
