import modules.screen.ocr as ocr
from modules.screen.pixelColor import getPixelColor
import modules.misc.appManager as appManager
import modules.misc.settingsManager as settingsManager
import time
import pyautogui as pag
from modules.controls.keyboard import keyboard
from modules.controls.sleep import sleep
import modules.controls.mouse as mouse
from modules.screen.screenData import getScreenData
from operator import itemgetter
import sys
import os

class macro:
    def __init__(self, status, log):
        self.status = status
        self.log = log
        self.setdat = settingsManager.loadAllSettings()
        self.fieldSettings = settingsManager.loadFields()
        self.mw, self.mh = pag.size()
        screenData = getScreenData()
        self.display_type, self.ww, self.wh, self.ysm, self.xsm, self.ylm, self.xlm = itemgetter("display_type", "screen_width","screen_height", "y_multiplier", "x_multiplier", "y_length_multiplier", "x_length_multiplier")(screenData)
        self.keyboard = keyboard(28)
    #run a path. Choose automater over python if it exists (except on windows)
    def runPath(self, name):
        path = f"../settings/paths/{name}"
        #try running a automator workflow
        #if it doesnt exist, run the .py file instead

        if os.path.exists(path+".workflow") and sys.platform == "darwin":
            os.system(f"/usr/bin/automator {path}.workflow")
        else:
            exec(open(f"{path}.py").read())
    #run the path to go to a field
    def goToField(self, field):
        self.runPath(f"cannon_to_field/{field}")

    def isBesideE(self, includeList = [], excludeList = []):
        #get text
        text = ocr.imToString("bee bear").lower()
        #check if text is to be rejected
        for i in excludeList:
            if i in text: return False
        #check if its to be accepted
        for i in includeList:
            if i in text:  return True
        return False
    
    def reset(self, hiveCheck = False, convert = True):
        yOffset = 0 #TODO: calculate yoffset
        #reset until player is at hive
        for i in range(5):
            #set mouse and execute hotkeys
            mouse.teleport(self.mw/(self.xsm*4.11)+40,(self.mh/(9*self.ysm))+yOffset)
            time.sleep(0.5)
            self.keyboard.press('esc')
            time.sleep(0.1)
            self.keyboard.press('r')
            time.sleep(0.2)
            self.keyboard.press('enter')
            time.sleep(8)
            #detect if player at hive
            if self.isBesideE(["make", "маке", "нопеу", "honey", "flower", "field"]):
                break
        #set the player's orientation to face hive, max 4 attempts
        for _ in range(4):
            pix = getPixelColor((self.ww//2)+20,self.wh-2)
            r = [int(x) for x in pix]
            avgDiff = (abs(r[2]-r[1])+abs(r[2]-r[0])+abs(r[1]-r[0]))/3
            if avgDiff < 15:
                for _ in range(8):
                    self.keyboard.press("o")
                return True
            
            for _ in range(4):
                self.keyboard.press(".")
                time.sleep(0.05)
        time.sleep(0.3)
    def cannon(self, fast = False):
        for i in range(3):
            #Move to canon:
            self.keyboard.walk("w",0.8)
            self.keyboard.walk("d",0.9*3) #(setdat["hive_number"])+1
            self.keyboard.keyDown("d")
            time.sleep(0.5)
            self.keyboard.slowPress("space")
            time.sleep(0.2)
            self.keyboard.keyDown("d")
            self.keyboard.walk("w",0.25)
            
            if fast:
                self.keyboard.walk("d",0.95)
                time.sleep(0.1)
                return
            self.keyboard.walk("d",0.35)
            self.keyboard.walk("s",0.07)
            for _ in range(6):
                self.keyboard.walk("d",0.2)
                time.sleep(0.05)
                if self.isBesideE(["fire","red"]):
                    #webhook("","Cannon found","dark brown")
                    return
            self.reset()
        else:
            print("cannon failed")
            disconnect = True
    def gather(self, field):
        self.status = "hi"
        fieldSetting = self.fieldSettings[field]
        #go to field
        self.cannon()
        self.goToField(field)
        #go to start location
        startLocationData = {
            "center": [],
            "upper right": ["w","d"],
            "right": ["d"],
            "lower right": ["s","d"],
            "bottom": ["s"],
            "lower left": ["s","a"],
            "left": ["a"],
            "upper left": ["w","a"]
        }
        self.keyboard.multiWalk(startLocationData[fieldSetting["start_location"]], fieldSetting["distance"]/4.7)
        #place sprinkler + check if in field
        #rotate camera
        #check invert L/R and invert B/R

    def start(self):
        #TODO: detect new/old ui and set 
        appManager.openApp("roblox")
        time.sleep(2)
        self.reset()
        self.gather("pine tree")
