import pyautogui as pag
import os
import tkinter
import move
import loadsettings

sizeword = setdat["gather_size"]
width = setdat["gather_width"]
size = 0
if sizeword.lower() == "s":
    size = 0.5
elif sizeword.lower() == "l":
    size =1.5
else:
    size = 1

'''
TCFBKey:=FwdKey W
    AFCFBKey:=BackKey S
    TCLRKey:=LeftKey A
    AFCLRKey:=RightKey D
'''
base = 0.3 #only edit this value
    
for _ in range(width):
    move.hold("d",base*size)
    move.hold("s",base*size*6.8)
    move.hold("d",base*size)
    move.hold("w",base*size*5.6)
    move.hold("d",base*size)
    move.hold("s",base*size*7.36)
    move.hold("d",base*size*1.6)
    move.hold("w",base*size*5.6)

for _ in range(width):
    move.hold("a",base*size)
    move.hold("s", base*size*6)
    move.hold("a",base*size*0.8)
    move.hold("w",base*size*5.6)
    move.hold("a",base*size)
    move.hold("s",base*size*7.2)
    move.hold("a",base*size)
    move.hold("w",base*size*5.6)
    
    
    
    



    
    
