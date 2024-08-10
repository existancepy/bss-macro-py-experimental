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
import modules.logging.log as logModule
from operator import itemgetter
import sys
import os
from threading import Thread
from modules.screen.backpack import bpc

class macro:
    def __init__(self, status, log):
        self.status = status
        self.setdat = settingsManager.loadAllSettings()
        self.fieldSettings = settingsManager.loadFields()
        self.mw, self.mh = pag.size()
        screenData = getScreenData()
        self.display_type, self.ww, self.wh, self.ysm, self.xsm, self.ylm, self.xlm = itemgetter("display_type", "screen_width","screen_height", "y_multiplier", "x_multiplier", "y_length_multiplier", "x_length_multiplier")(screenData)
        self.keyboard = keyboard(self.setdat["movespeed"]) #TODO: implement haste compensation
        self.logger = logModule.log(log)

    #run a path. Choose automater over python if it exists (except on windows)
    def runPath(self, name):
        ws = self.setdat["movespeed"]
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

    def isInOCR(self, name, includeList, excludeList):
        #get text
        text = ocr.imToString(name).lower()
        #check if text is to be rejected
        for i in excludeList:
            if i in text: return False
        #check if its to be accepted
        for i in includeList:
            if i in text:  return text
        return False
    
    def isBesideE(self, includeList = [], excludeList = []):
        return self.isInOCR("bee bear", includeList, excludeList)
    
    def isInBlueTexts(self, includeList = [], excludeList = []):
        return self.isInOCR("blue", includeList, excludeList)
    
    #place sprinklers by jumping up and down and placing them middair
    def placeSprinkler(self):
        sprinklerCount = {
            "basic":1,
            "silver":2,
            "golden":3,
            "diamond":4,
            "saturator":1
        }
        sprinklerSlot = str(self.setdat['sprinkler_slot'])
        times = sprinklerCount[self.setdat["sprinkler_type"]]
        #place one sprinkler and check if its in field
        self.keyboard.press(sprinklerSlot)
        time.sleep(0.3)
        if self.isInBlueTexts(["must", "standing", "place"]):
            return False
        #place the remaining sprinklers
        #hold jump and spam place sprinklers
        if times > 1:
            self.keyboard.keyDown("space")
            st = time.time()
            while time.time() - st < times*2:
                self.keyboard.press(sprinklerSlot)
            self.keyboard.keyUp("space")
        return True
    
    def convert(self, bypass = False):
        if not bypass:
            if not self.isBesideE(["make", "маке"], ["to"]): return
        self.logger.webhook("", "Converting", "brown")
        self.keyboard.press("e")
        st = time.time()
        time.sleep(2)
        while True:
            if not self.isBesideE(["stop"]): 
                self.logger.webhook("", "Finished converting", "brown")
                break
            if time.time() - st > 600:
                self.logger.webhook("", "Converting took too long, moving on", "brown")
                break

    def reset(self, hiveCheck = False, convert = True):
        self.keyboard.releaseMovement()
        yOffset = 20 #TODO: calculate yoffset
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
            self.logger.webhook("", f"Resetting character, Attempt: {i+1}", "dark brown")
            besideE = self.isBesideE(["make", "маке", "нопеу", "honey", "flower", "field"])
            if besideE: break
        else:
            self.logger.webhook("Notice", f"Unable to detect that player respawned at hive, continuing", "red")
            return False

        #set the player's orientation to face hive, max 4 attempts
        for _ in range(4):
            pix = getPixelColor((self.ww//2)+20,self.wh-2)
            r = [int(x) for x in pix]
            avgDiff = (abs(r[2]-r[1])+abs(r[2]-r[0])+abs(r[1]-r[0]))/3
            if avgDiff < 15:
                for _ in range(8):
                    self.keyboard.press("o")
                #convert if enabled
                if ("make" in besideE or "маке" in besideE) and not "to" in besideE:
                    self.convert(True)
                return True
            
            for _ in range(4):
                self.keyboard.press(".")
                time.sleep(0.05)
        time.sleep(0.3)
        self.logger.webhook("Notice", f"Unable to detect the direction the player is facing, continuing", "red")
        return False

    def cannon(self, fast = False):
        for i in range(3):
            #Move to canon:
            self.keyboard.walk("w",0.8)
            self.keyboard.walk("d",0.9*(self.setdat["hive_number"]+1))
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
                    return
            self.logger.webhook("Notice", f"Could not find cannon", "red")
            self.reset()
        else:
            self.logger.webhook("Notice", f"Failed to reach cannon too many times", "red")
            disconnect = True
    def gather(self, field):
        fieldSetting = self.fieldSettings[field]
        for i in range(3):
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
                "upper left": ["w","a"],
                "top": ["w"]
            }
            self.keyboard.multiWalk(startLocationData[fieldSetting["start_location"]], fieldSetting["distance"]/4)
            #place sprinkler + check if in field
            if self.placeSprinkler(): 
                break
            self.logger.webhook("Notice", f"Failed to land in field", "red")
            self.reset()
        #rotate camera
        if fieldSetting["turn"] == "left":
            for _ in range(fieldSetting["turn_times"]):
                self.keyboard.press(",")
        elif fieldSetting["turn"] == "right":
            for _ in range(fieldSetting["turn_times"]):
                self.keyboard.press(".")
        #key variables
        #check invert L/R and invert B/R
        fwdkey = "w"
        leftkey = "a" 
        backkey = "s" 
        rightkey = "d"
        rotleft = ","
        rotright = "."
        rotup = "pageup"
        rotdown = "pagedown"
        zoomin = "i"
        zoomout = "o"
        sc_space = "space"
        tcfbkey = fwdkey
        afcfbkey = backkey
        tclrkey = leftkey
        afclrkey = rightkey
        if fieldSetting["invert_lr"]:
            tclrkey = rightkey
            afclrkey = leftkey
        if fieldSetting["invert_fb"]:
            tcfbkey = backkey
            afcfbkey = fwdkey
        facingcorner = 0
        sizeData = {
            "xs": 0.25,
            "s": 0.5,
            "m": 1,
            "l": 1.5,
            "xl": 2
        }
        sizeword = fieldSetting["size"]
        size = sizeData[sizeword]
        width = fieldSetting["width"]
        maxGatherTime = 0 #fieldSetting["mins"]*60
        gatherTimeLimit = "{:.2f}".format(fieldSetting["mins"])
        returnType = fieldSetting["return"]
        st = time.time()
        keepGathering = True
        #time to gather
        self.logger.webhook(f"Gathering: {field.title()}", f"Limit: {gatherTimeLimit} - {fieldSetting['shape']} - Backpack: {fieldSetting['backpack']}%", "light green")
        while keepGathering:
            if fieldSetting["shift_lock"]: self.keyboard.press('shift')
            mouse.mouseDown()
            exec(open(f"../settings/patterns/{fieldSetting['shape']}.py").read())
            #cycle ends
            mouse.mouseUp()
            if fieldSetting["shift_lock"]: self.keyboard.press('shift')
            #check if max time is reached
            if time.time() - st > maxGatherTime:
                self.logger.webhook(f"Gathering: Ended", f"Time: {gatherTimeLimit} - Time Limit - Return: {returnType}", "light green")
                keepGathering = False
            #check backpack
            if bpc(self.ww, False, self.display_type) >= fieldSetting["backpack"]:
                self.logger.webhook(f"Gathering: Ended", f"Time: {gatherTimeLimit} - Backpack - Return: {returnType}", "light green")
                keepGathering = False
        '''
        if returnType == "reset":
            self.reset(convert=True)
        elif returnType == "rejoin":
            pass
        '''
        if returnType:
            #walk to hive
            #face correct direction (towards hive)
            reverseTurnTimes = 4 - fieldSetting["turn_times"]
            if fieldSetting["turn"] == "none":
                reverseTurnTimes = 4
            if fieldSetting["turn"] == "left":
                for _ in range(reverseTurnTimes):
                    self.keyboard.press(",")
            else: #right or none
                for _ in range(reverseTurnTimes):
                    self.keyboard.press(".")

            #start walk
            self.logger.webhook("",f"Walking back to hive: {field.title()}", "dark brown")
            self.runPath(f"field_to_hive/{field}")
            #find hive and convert
            self.keyboard.walk("a", (self.setdat["hive_number"]-1)*0.9)
            for _ in range(30):
                self.keyboard.walk("a",0.2)
                time.sleep(0.15)
                if self.isBesideE(["make", "маке"]):
                    self.convert(bypass=True)
                    self.reset(convert=False)
                    break
            else:
                self.logger.webhook("","Can't find hive, resetting", "dark brown")
                self.reset()


    def start(self):
        print(self.status.value)
        #TODO: detect new/old ui and set 
        appManager.openApp("roblox")
        time.sleep(2)
        self.reset(convert=True)
