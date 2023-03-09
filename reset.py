import pyautogui as pag
import time
import os
import tkinter
import imagesearch
from webhook import webhook
import loadsettings
from delay import sleep
from pynput.mouse import Button, Controller
from pynput.keyboard import Key
import pynput.keyboard
keyboard = pynput.keyboard.Controller()
mouse = Controller()
savedata = {}
mw,mh = pag.size()
def loadSave():
    with open('save.txt') as f:
        lines = f.read().split("\n")
    f.close()
    for s in lines:
        l = s.replace(" ","").split(":")
        if l[1].isdigit():
            l[1] = int(l[1])
        savedata[l[0]] = l[1]

def reset():
    setdat = loadsettings.load()
    ths = setdat["hivethreshold"]
    rhd = setdat["reverse_hive_direction"]
    ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
    xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
    print("ths is {}".format(ths))
    loadSave()
    for i in range(2):
        webhook("","Resetting character, Attempt: {}".format(i+1),"dark brown")
        mouse.position = (mw/(xsm*4.11),mh/(9*ysm))
        ww = savedata["ww"]
        wh = savedata["wh"]
        xo = ww//4
        yo = wh//4*3
        xt = xo*3-xo
        yt = wh-yo
        time.sleep(0.5)
        pag.press('esc')
        time.sleep(0.1)
        keyboard.press('r')
        keyboard.release('r')
        time.sleep(0.1)
        pag.press('enter')
        sleep(8.5)
        for _ in range(4):
            keyboard.press(Key.page_up)
            keyboard.release(Key.page_up)
        time.sleep(0.1)
        for _ in range(6):
            keyboard.press('o')
            time.sleep(0.08)
            keyboard.release('o')
        #im = pag.screenshot(region = (xo,yo,xt,yt))
        #im.save('a.png')
        for _ in range(4):
            r = imagesearch.find("hive1.png",ths, xo, yo, xt, yt)
            if r:
                time.sleep(0.1)
                if not rhd:
                    for _ in range(4):
                        keyboard.press(',')
                        keyboard.release(',')

                time.sleep(0.1)
                for _ in range(4):
                    keyboard.press(Key.page_down)
                    keyboard.release(Key.page_down)
                return
            for _ in range(4):
                keyboard.press(',')
                keyboard.release(',')
            
            time.sleep(0.5)
        time.sleep(1)
    '''
    for _ in range(4):
        pag.press(",")
    webhook("","Cannot find hive. Now undergoing threshold method.","dark brown",1)
    vals = []
    for _ in range(1):
        webhook("","Obtaining values","dark brown")
        time.sleep(2)
        pag.press('esc')
        time.sleep(0.1)
        pag.press('r')
        time.sleep(0.2)
        pag.press('enter')
        sleep(8)
        for _ in range(4):
            pag.press('pgup')
        time.sleep(0.1)
        for _ in range(6):
            pag.press('o')
        #im = pag.screenshot(region = (xo,yo,xt,yt))
        #im.save('a.png')

        time.sleep(0.4)
        for _ in range(4):
            r = imagesearch.find("hive1.png",0, xo, yo, xt, yt)
            vals.append(r[3])
            for _ in range(4):
                pag.press(",")
            
            time.sleep(0.5)
        time.sleep(1)
    vals = sorted(vals,reverse=True)
    print(vals)
    thresh = (vals[1]+vals[2])/2
    webhook("","threshold calculated. Value of {}".format(thresh),"dark brown")
    webhook("","Now attempting to find hive","dark brown")
    for _ in range(1):
        time.sleep(2)
        pag.press('esc')
        time.sleep(0.1)
        pag.press('r')
        time.sleep(0.2)
        pag.press('enter')
        sleep(8.5)
        for _ in range(4):
            pag.press('pgup')
        time.sleep(0.1)
        for _ in range(6):
            pag.press('o')
        #im = pag.screenshot(region = (xo,yo,xt,yt))
        #im.save('a.png')

        time.sleep(0.4)
        for _ in range(4):
            r = imagesearch.find("hive1.png",thresh, xo, yo, xt, yt)
            if r:
                time.sleep(0.1)
                if not rhd:
                    for _ in range(4):
                        pag.press(".")

                time.sleep(0.1)
                for _ in range(4):
                    pag.press('pgdn')
                return True
            for _ in range(4):
                pag.press(",")
            
            time.sleep(0.5)
        time.sleep(1)
    for _ in range(4):
        pag.press(",")
    '''
    return False
    webhook("Notice","Hive not found. Assume that player is facing the right direction","red",1)

def resetCheck():
    ths = loadsettings.load()["hivethreshold"]
    loadSave()
    ysm = loadsettings.load('multipliers.txt')['y_screenshot_multiplier']
    xsm = loadsettings.load('multipliers.txt')['x_screenshot_multiplier']
    for _ in range(2):
        webhook("","Resetting character","dark brown")
        pag.moveTo(mw/(4.11*xsm),mh/(9*ysm))
        ww = savedata["ww"]
        wh = savedata["wh"]
        xo = ww//4
        yo = wh//100*90
        xt = xo*2
        yt = wh//100*20
        time.sleep(2)
        pag.press('esc')
        time.sleep(0.1)
        pag.press('r')
        time.sleep(0.2)
        pag.press('enter')
        sleep(8.5)
        for _ in range(4):
            pag.press('pgup')
        time.sleep(0.1)
        for _ in range(6):
            pag.press('o')
        #im = pag.screenshot(region = (xo,yo,xt,yt))
        #im.save('a.png')

        time.sleep(0.4)
        for _ in range(4):
            r = imagesearch.find("hive1.png",ths, xo, yo, xt, yt)
            if r:
                time.sleep(0.1)
                for _ in range(4):
                    pag.press(".")

                time.sleep(0.1)
                for _ in range(4):
                    pag.press('pgdn')
                return True
            for _ in range(4):
                pag.press(",")
            
            time.sleep(0.5)
        time.sleep(1)
    for _ in range(4):
        pag.press(",")
    webhook("Notice","Hive not found.","red",1)
    return False


