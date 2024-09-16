import modules.screen.ocr as ocr
from modules.screen.pixelColor import getPixelColor
import modules.misc.appManager as appManager
import modules.misc.settingsManager as settingsManager
import time
import pyautogui as pag
from modules.screen.screenshot import mssScreenshot, mssScreenshotNP
from modules.controls.keyboard import keyboard
from modules.controls.sleep import sleep
import modules.controls.mouse as mouse
from modules.screen.screenData import getScreenData
import modules.logging.log as logModule
from modules.submacros.fieldDriftCompensation import fieldDriftCompensation as fieldDriftCompensationClass
from operator import itemgetter
import sys
import platform
import os
import numpy as np
import threading
from modules.submacros.backpack import bpc
from modules.screen.imageSearch import *
import webbrowser
from pynput.keyboard import Key, Controller
import cv2
from datetime import timedelta, datetime
from modules.misc.imageManipulation import *
from PIL import Image
from modules.misc import messageBox
pynputKeyboard = Controller()
#data for collectable objectives
#[besideE text, movement key, max cooldowns]
collectData = { 
    "wealth_clock": [["use"], "w", 1*60*60], #1hr
    "blueberry_dispenser": [["use", "dispenser"], "a", 4*60*60], #4hr
    "strawberry_dispenser": [["use", "dispenser"], None, 4*60*60], #4hr
    "royal_jelly_dispenser": [["claim", "royal"], "a",22*60*60], #22hr
    "treat_dispenser": [["use", "treat"], "w", 1*60*60], #1hr
    "ant_pass_dispenser": [["use", "free"], "a", 2*60*60], #2hr
    "glue_dispenser": [["use", "glue"], None, 22*60*60], #22hr
    "stockings": [["check", "inside", "stocking"], "a", 1*60*60], #1hr
    "wreath": [["admire", "honey"], "a", 30*60], #30mins
    "feast": [["dig", "beesmas"], "s", 1.5*60*60], #1.5hr
    "samovar": [["heat", "samovar"], "w", 6*60*60], #6hr
    "snow_machine": [["activate"], None, 2*60*60], #2hr
    "lid_art": [["gander", "onett", "art"], "s", 8*60*60], #8hr
    "candles": [["admire", "candle", "honey"], "w", 4*60*60] #4hr
}

#werewolf is a unique one. There is only one, but it can be triggered from pine, pumpkin or cactus
regularMobInFields = {
    "rose": ["scorpion"],
    "pumpkin": ["werewolf"],
    "cactus": ["werewolf"],
    "spider": ["spider"],
    "clover": ["ladybug", "rhinobeetle"],
    "strawberry": ["ladybug"],
    "bamboo": ["rhinobeetle"],
    "mushroom": ["ladybug"],
    "blue flower": ["rhinobeetle"],
    "pineapple": ["mantis", "rhinobeetle"],
    "pine tree": ["mantis", "werewolf"],
}

mobRespawnTimes = {
    "ladybug": 5*60, #5mins
    "rhinobeetle": 5*60, #5mins
    "spider": 30*60, #30mins
    "mantis": 20*60, #20mins
    "scorpion": 20*60, #20mins
    "werewolf": 60*60 #1hr
}

# Define the color range for reset detection (in HSL color space)
resetLower = np.array([0, 102, 0])  # Lower bound of the color (H, L, S)
resetUpper = np.array([40, 255, 7])  # Upper bound of the color (H, L, S)
resetKernel = cv2.getStructuringElement(cv2.MORPH_RECT,(16,10))


nightFloorDetectThresholds = [
    [np.array([99, 45, 102]), np.array([105, 51, 112])], #starter fields, spawn
    [np.array([80, 15, 114]), np.array([100, 20, 130])], #clover, 15 bee gate, 10 bee gate, 35 bee gate
    []
]
locationToNightFloorType = {
    "spawn": 0,
    "sunflower": 0,
    "dandelion": 0,
    "mushroom": 0,
    "blue_flower": 0,
    "clover": 1,
    "strawberry": 2,
    "spider": 2,
    "bamboo": 2,
    "pineapple": 1,
    "stump": 1,
    "cactus": 1,
    "pumpkin": 1,
    "pine_tree": 1,
    "rose": 2,
    "mountain top": 3,
    "pepper": 1,
    "coconut": 1
}

#store planter's growth data
#[growth time in secs, (list of bonus fields), bonus growth from fields]
planterGrowthData = {
    "paper": [1*60*60, ()], #1hr
    "ticket": [2*60*60, ()], #2hr
    "festive": [4*60*60, ()], #4hr
    "sticker": [3*60*60, ()], #3hr
    "plastic": [2*60*60, ()], #2hr
    "candy": [4*60*60, ("strawberry", "pineapple", "coconut"), 0.25], #4hr
    "red clay": [6*60*60, ("sunflower", "dandelion", "mushroom", "clover", "strawberry", "pineapple", "stump", "cactus", "pumpkin", "rose", "mountain top", "pepper", "coconut"), 0.25], #6hr
    "blue clay": [6*60*60, ("sunflower", "dandelion", "blue flower", "clover", "bamboo", "pineapple", "stump", "cactus", "pumpkin", "pine tree", "mountain top", "coconut"), 0.25], #6hr
    "tacky": [8*60*60, ("sunflower", "dandelion", "mushroom", "blue flower", "clover"), 0.25], #8hr
    "pesticide": [10*60*60, ("bamboo", "spider", "strawberry"), 0.3], #10hr
    "heat-treated": [12*60*60, ("sunflower", "dandelion", "mushroom", "clover", "strawberry", "pineapple", "stump", "cactus", "pumpkin", "rose", "mountain top", "pepper", "coconut"), 0.5], #12hr
    "hydroponic": [12*60*60, ("sunflower", "dandelion", "blue flower", "clover", "bamboo", "pineapple", "stump", "cactus", "pumpkin", "pine tree", "mountain top", "coconut"), 0.5], #12hr
    "petal": [14*60*60, ("sunflower", "dandelion", "blue flower", "mushroom" "clover", "bamboo", "strawberry", "pineapple", "stump", "cactus", "pumpkin", "pine tree", "rose", "mountain top", "coconut", "pepper"), 0.5], #14hrs
    "planter of plenty": [16*60*60, ("pepper", "stump", "coconut", "mountain top"), 0.5] #16hr
}

class macro:
    def __init__(self, status, log, haste):
        self.status = status
        self.setdat = settingsManager.loadAllSettings()
        self.fieldSettings = settingsManager.loadFields()
        self.mw, self.mh = pag.size()
        screenData = getScreenData()
        self.display_type, self.ww, self.wh, self.ysm, self.xsm, self.ylm, self.xlm = itemgetter("display_type", "screen_width","screen_height", "y_multiplier", "x_multiplier", "y_length_multiplier", "x_length_multiplier")(screenData)
        self.keyboard = keyboard(self.setdat["movespeed"], haste)
        self.logger = logModule.log(log, self.setdat["enable_webhook"], self.setdat["webhook_link"])
        #setup an internal cooldown tracker. The cooldowns can be modified
        self.collectCooldowns = dict([(k, v[2]) for k,v in collectData.items()])
        self.collectCooldowns["sticker_printer"] = 1*60*60

        #field drift compensation class
        self.fieldDriftCompensation = fieldDriftCompensationClass(self.display_type == "retina")

        #night detection variables
        self.canDetectNight = True
        self.night = False
        self.location = "spawn"
        #all fields that vic can appear in
        self.vicFields = ["pepper", "mountain top", "rose", "cactus", "spider", "clover"]
        #filter it to only include fields the player has enabled
        self.vicFields = [x for x in self.vicFields if self.setdat["stinger_{}".format(x.replace(" ","_"))]]

        self.newUI = False

        self.planterCooldowns = {}

    #thread to detect night
    #night detection is done by converting the screenshot to hsv and checking the average brightness
    #TODO:
    # MAYBE this doesnt actually need to be a thread? Check for night after each reset, when converting and when gathering
    def detectNight(self):
        #detects the average brightness of the screen. This isn't very reliable since things like lights can mess it up
        #the threshold isnt accurate
        def isNightBrightness(hsv):
            vValues = np.sum(hsv[:, :, 2])
            area = hsv.shape[0] * hsv.shape[1]
            avg_brightness = vValues/area
            return 10 < avg_brightness < 120 #threshold for night. It must be > 10 to deal with cases where the player is inside a fruit or stuck against a wall 

        #Detect the color of the floor at spawn
        #Useful when resetting/converting
        def isSpawnFloorNight(hsv):
            lower = np.array([99, 45, 102])
            upper = np.array([105, 51, 112])

            #might increase kernel size on retina
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(15,15))

            mask = cv2.inRange(hsv, lower, upper)   
            mask = cv2.erode(mask, kernel, 2)

            #if np.mean = 0, no color ranges are detected, is day, hence return false
            return np.mean(mask)
        
        def isNightSky(bgr):
            y = 30
            if self.display_type == "retina": y*=2
            #crop the image to only the area above buff
            bgr = bgr[0:y, 0:int(self.mw)]
            w,h = bgr.shape[:2]
            #check if a 15x15 area that is entirely black
            for x in range(w-15):
                for y in range(h-15):
                    area = bgr[x:x+15, y:y+15]
                    if np.all(area == [0, 0, 0]):
                        return True
            return False
        
        #detect the color of the grass in fields
        #useful when gathering
        def isGrassNight(hsv):
            def threshold(lower, upper):
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(4,4))
                mask = cv2.inRange(hsv, lower, upper)   
                mask = cv2.erode(mask, kernel, 1)
                return bool(np.mean(mask))
            
            def grassDay():
                dayLower = np.array([63, 127, 140]) 
                dayUpper = np.array([68, 165, 163])
                return threshold(dayLower, dayUpper)
            
            def grassNight():
                nightLower = np.array([65, 183, 51]) 
                nightUpper = np.array([68, 204, 77])
                return threshold(nightLower, nightUpper)
            
            if grassDay(): return False
            if grassNight(): return True
            return False

        def isNight():
            screen = mssScreenshotNP(0,0, self.mw, self.mh)
            # Convert the image from BGRA to HSV
            bgr = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
            hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

            #detect brightness
            if not isNightBrightness(hsv): return False
            if self.location == "spawn":
                return isSpawnFloorNight(hsv)
            return isGrassNight(hsv) and isNightSky(bgr)
        
        while True:
            if self.canDetectNight and isNight():
                self.night = True
                self.logger.webhook("","Night detected","dark brown", "screen")
                time.sleep(200) #wait for night to end
                self.night = False

    def isFullScreen(self):
        menubarRaw = ocr.customOCR(0, 0, 300, 60, 0) #get menu bar on mac, window bar on windows
        print(menubarRaw)
        menubar = ""
        try:
            for x in menubarRaw:
                menubar += x[1][0]
        except:
            pass
        menubar = menubar.lower()
        print(menubar)
        return not ("rob" in menubar or "lox" in menubar) #check if roblox can be found in menu bar

    def toggleFullScreen(self):
        if sys.platform == "darwin":
            self.keyboard.keyDown("command")
            time.sleep(0.05)
            self.keyboard.keyDown("ctrl")
            time.sleep(0.05)
            self.keyboard.keyDown("f")
            time.sleep(0.1)
            self.keyboard.keyUp("command")
            self.keyboard.keyUp("ctrl")
            self.keyboard.keyUp("f")
        elif sys.platform == "win32":
            for _ in range(3):
                self.keyboard.press("f11")
                time.sleep(0.4)

    def adjustImage(self, path, imageName):
        return adjustImage(path, imageName, self.display_type)
        
    #run a path. Choose automater over python if it exists (except on windows)
    #file must exist: if set to False, will not attempt to run the file if it doesnt exist
    def runPath(self, name, fileMustExist = True):
        ws = self.setdat["movespeed"]
        path = f"../settings/paths/{name}"
        #try running a automator workflow
        #if it doesnt exist, run the .py file instead

        if os.path.exists(path+".workflow") and sys.platform == "darwin":
            os.system(f"/usr/bin/automator {path}.workflow")
        else:
            pyPath = f"{path}.py"
            #ensure that path exists
            if not fileMustExist and not os.path.isfile(pyPath): return
            exec(open(pyPath).read())
    #run the path to go to a field
    def goToField(self, field):
        self.location = field
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
    
    def isBesideEImage(self, name):
        template = self.adjustImage("./images/menu",name)
        return locateTransparentImageOnScreen(template, self.mw//2-200,0,400,self.mh//8, 0.75)

    def getTiming(self,name = None):
        for _ in range(3):
            data = settingsManager.readSettingsFile("./data/user/timings.txt")
            if data: break #most likely another process is writing to the file
            time.sleep(0.1)
        if name is not None:
            return data[name]
        return data
    
    def saveTiming(self, name):
        return settingsManager.saveSettingFile(name, time.time(), "./data/user/timings.txt")
    #returns true if the cooldown is up
    #note that cooldown is in seconds
    def hasRespawned(self, name, cooldown, applyMobRespawnBonus = False, timing = None):
        if timing is None: timing = self.getTiming(name)
        mobRespawnBonus = 1
        if applyMobRespawnBonus:
            mobRespawnBonus -= 0.15 if self.setdat["gifted_vicious"] else 0
            mobRespawnBonus -= self.setdat["stick_bug_amulet"]/100 
            mobRespawnBonus -= self.setdat["icicles_beequip"]/100 

        return time.time() - timing >= cooldown*mobRespawnBonus

    def isInBlueTexts(self, includeList = [], excludeList = []):
        return self.isInOCR("blue", includeList, excludeList)
    
    #detect the honey/pollen bar to determine if its new or old ui
    def getTop(self,y):
        height = 30
        if self.display_type == "retina":
            height*=2
            y*=2
        res = ocr.customOCR(self.ww/3.5,y,self.ww/2.5,height,0)
        if not res: return False
        text = ''.join([x[1][0].lower() for x in res])
        return "honey" in text or "pollen" in text
    
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
        time.sleep(1)
        if self.blueTextImageSearch("notinfield"):
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
    
    def clickYes(self):
        yesImg = self.adjustImage("./images/menu", "yes")
        x = self.mw/3.2
        y = self.mh/2.3
        time.sleep(0.4)
        bestX, bestY = locateImageOnScreen(yesImg,x,y,self.mw/2.5,self.mh/3.4)[1]
        if self.display_type == "retina":
            bestX //=2
            bestY //=2
        mouse.moveTo(bestX+x, bestY+y)
        time.sleep(0.2)
        mouse.moveBy(5, 5)
        time.sleep(0.1)
        for _ in range(2):
            mouse.click()
    
    def toggleInventory(self):
        mouse.moveTo(30, 113)
        time.sleep(0.1)
        mouse.click()
        time.sleep(0.2)
        self.moveMouseToDefault()
        '''
        self.keyboard.press("\\")
        #align with first buff
        for _ in range(7):
            self.keyboard.press("w")
        for _ in range(20):
            self.keyboard.press("a")
        #open inventory
        if sys.platform == "darwin":
            for _ in range(5):
                self.keyboard.press("w")
                time.sleep(0.1)
            self.keyboard.press("s")
            self.keyboard.press("a")
            time.sleep(0.1)
            self.keyboard.press("enter")
        else:
            self.keyboard.press("s")
            self.keyboard.press("enter")
        '''

    #scroll to an item in the inventory and return the x,y coordinates
    def findItemInInventory(self, itemName):
        itemImg = self.adjustImage("./images/inventory", itemName)
        #open inventory
        self.toggleInventory()
        time.sleep(0.3)
        mouse.moveTo(312, 200)
        mouse.click()
        #scroll to top
        for _ in range(80):
            mouse.scroll(100)
        #scroll down, note the best match
        bestScroll, bestX, bestY = None, None, None
        valBest = 0
        foundEarly = False #if the max_val > 0.9, end searching early to save time
        time.sleep(0.3)
        for i in range(60):
            max_val, max_loc = locateImageOnScreen(itemImg, 0, 90, 120, self.mh-180)
            if max_val > valBest:
                valBest = max_val
                bestX, bestY = max_loc
                bestScroll = i
                if max_val > 0.9:
                    foundEarly = True
                    break
            mouse.scroll(-40, True)
            time.sleep(0.04)
        if valBest < 0.55:
            self.logger.webhook("", f"Could not find {itemName} in inventory", "dark brown")
            return None
        if not foundEarly:
            #scroll to the top
            for _ in range(80):
                mouse.scroll(100)
            time.sleep(0.3)
            #scroll to item
            for _ in range(bestScroll):
                mouse.scroll(-40, True)
        if self.display_type == "retina":
            bestX //= 2
            bestY //= 2
        return (bestX+20, bestY+80+20)
    
    #click at the specified coordinates to use an item in the inventory
    #if x/y is not provided, find the item in inventory
    def useItemInInventory(self, itemName = None, x = None, y = None):
        if x is None or y is None:
            if itemName is None: raise Exception("tried searching for item but no item name is provided")
            res = self.findItemInInventory(itemName)
            if res is None:
                self.toggleInventory()
                return False
            x, y = res
        #close UI navigation
        mouse.moveTo(x, y)
        for _ in range(2):
            mouse.click()
        mouse.moveBy(10,10)
        mouse.click()
        self.clickYes()
        #close inventory
        self.toggleInventory()
        return True


    def convert(self, bypass = False):
        self.location = "spawn"
        if not bypass:
            #use ebutton detection, faster detection but more prone to false positives (like detecting trades)
            if not self.isBesideEImage("makehoney"): return False
        #start convert
        self.keyboard.press("e")
        st = time.time()
        time.sleep(2)
        self.logger.webhook("", "Converting", "brown", "screen")
        while not self.isBesideE(["pollen", "flower", "field"]): 
            mouse.click()
            if self.night and self.setdat["stinger_hunt"]:
                self.stingerHunt()
                return
        #deal with the extra delay
        self.logger.webhook("", "Finished converting", "brown")
        wait = self.setdat["convert_wait"]
        if (wait):
            self.logger.webhook("", f'Waiting for an additional {wait} seconds', "light green")
        time.sleep(wait)
        return True

    def moveMouseToDefault(self):
        yOffset = 0
        if self.newUI: yOffset += 20
        mouse.moveTo(370, 100+yOffset)

    def reset(self, hiveCheck = False, convert = True):
        self.keyboard.releaseMovement()

        #reset until player is at hive
        for i in range(5):
            self.logger.webhook("", f"Resetting character, Attempt: {i+1}", "dark brown")
            #set mouse and execute hotkeys
            #mouse.teleport(self.mw/(self.xsm*4.11)+40,(self.mh/(9*self.ysm))+yOffset)
            self.canDetectNight = False

            #close any menus if they exist
            closeImg = self.adjustImage("./images/menu", "close") #sticker printer
            if locateImageOnScreen(closeImg, self.mw/4, 100, self.mw/4, self.mh/3.5, 0.7):
                self.keyboard.press("e")

            self.moveMouseToDefault()
            time.sleep(0.1)
            self.keyboard.press('esc')
            time.sleep(0.1)
            self.keyboard.press('r')
            time.sleep(0.2)
            self.keyboard.press('enter')
            emptyHealth = self.adjustImage("./images/menu", "emptyhealth")
            st = time.time()
            #wait for empty health bar to appear
            while time.time() - st < 3 and not locateImageOnScreen(emptyHealth, self.mw-100, 0, 100, 60, 0.7): pass
            #if the empty health bar disappears, player has respawned
            #max 8s in case player does not respawn
            st = time.time()
            while time.time() - st < 9:
                if not locateImageOnScreen(emptyHealth, self.mw-100, 0, 100, 60, 0.7):
                    time.sleep(0.5)
                    break

            self.canDetectNight = True
            self.location = "spawn"
            #detect if player is at hive. Spin a max of 4 times
            for _ in range(4):
                screen = pillowToCv2(mssScreenshot(self.mw//2-100, self.mh-10, 200, 10))
                # Convert the image from BGR to HLS color space
                hsl = cv2.cvtColor(screen, cv2.COLOR_BGR2HLS)
                # Create a mask for the color range
                mask = cv2.inRange(hsl, resetLower, resetUpper)   
                mask = cv2.erode(mask, resetKernel, 2)
                #get contours. If contours exist, direction is correct
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if contours:
                    for _ in range(8):
                        self.keyboard.press("o")
                    if convert: self.convert()
                    return True
                #failed to detect, spin
                for _ in range(4):
                    self.keyboard.press(".")
                time.sleep(0.1)
        else:
            self.logger.webhook("Notice", f"Unable to detect that player respawned at hive. Ensure that terminal has accessibility and screen recording permissions", "red", "screen")
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
            self.keyboard.walk("w",0.2)
            
            if fast:
                self.keyboard.walk("d",0.95)
                time.sleep(0.1)
                return
            self.keyboard.walk("d",0.2)
            self.keyboard.walk("s",0.07)
            st = time.time()
            self.keyboard.keyDown("d")
            while time.time()-st < 0.15*6:
                if self.isBesideEImage("cannon"):
                    self.keyboard.keyUp("d")
                    return
            self.keyboard.keyUp("d")
            self.logger.webhook("Notice", f"Could not find cannon", "dark brown", "screen")
            self.reset(convert=False)
        else:
            self.logger.webhook("Notice", f"Failed to reach cannon too many times", "red")
    
    def rejoin(self, rejoinMsg = "Rejoining"):
        self.canDetectNight = False
        psLink = self.setdat["private_server_link"]
        self.logger.webhook("",rejoinMsg, "dark brown")
        mouse.mouseUp()
        keyboard.releaseMovement()
        for i in range(3):
            rejoinMethod = self.setdat["rejoin_method"]
            browserLink = "https://www.roblox.com/games/4189852503?privateServerLinkCode=87708969133388638466933925137129"
            if psLink: 
                if i == 2: 
                    self.logger.webhook("", "Failed rejoining too many times, falling back to a public server", "red", "screen")
                else:
                    browserLink = psLink
            appManager.closeApp("Roblox") # close roblox
            time.sleep(8)
            #execute rejoin method
            if rejoinMethod == "deeplink":
                deeplink = "roblox://placeID=1537690962"
                if psLink:
                    deeplink += f"&linkCode={psLink.lower().split('code=')[1]}"
                appManager.openDeeplink(deeplink)
            elif rejoinMethod == "new tab":
                print(browserLink)
                webbrowser.open(browserLink, new = 2)
            elif rejoinMethod == "reload":
                webbrowser.open(browserLink, new = 2)
                time.sleep(2)
                if sys.platform == "darwin":
                    self.keyboard.keyDown("command")
                else:
                    self.keyboard.keyDown("ctrl")
                self.keyboard.press("r")
                if sys.platform == "darwin":
                    self.keyboard.keyUp("command")
                else:
                    self.keyboard.keyUp("ctrl")
            #wait for bss to load
            #if sprinkler image is found, bss is loaded
            #max 60s of waiting
            sprinklerImg = self.adjustImage("./images/menu", "sprinkler")
            loadStartTime = time.time()
            while not locateImageOnScreen(sprinklerImg, self.mw//2-300, self.mh*3/4, 300, self.mh*1/4, 0.75) and time.time() - loadStartTime < 60:
                pass
            #run fullscreen check
            if self.isFullScreen(): #check if roblox can be found in menu bar
                self.logger.webhook("","Roblox is already in fullscreen, not activating fullscreen", "dark brown")
            else:
                self.logger.webhook("","Roblox is not in fullscreen, activating fullscreen", "dark brown")
                self.toggleFullScreen()

            #if use browser to rejoin, close the browser
            if self.setdat["rejoin_method"] != "deeplink":
                time.sleep(2)
                webbrowser.open("https://docs.python.org/3/library/webbrowser.html", autoraise=True)
                time.sleep(0.5)
                for _ in range(2):
                    if sys.platform == "darwin":
                        self.keyboard.keyDown("command")
                    else:
                        self.keyboard.keyDown("ctrl")
                    self.keyboard.press("w")
                    if sys.platform == "darwin":
                        self.keyboard.keyUp("command")
                    else:
                        self.keyboard.keyUp("ctrl")
                    time.sleep(0.5)
                appManager.openApp("Roblox")
            else:
                #check if the user is stuck on the sign up screen
                signUpImage = self.adjustImage("./images/menu", "signup")
                if locateImageOnScreen(signUpImage, self.mw/4, self.mh/3, self.mw/2, self.mh*2/3, 0.7):
                    self.logger.webhook("","Not logged into the roblox app. Rejoining via the browser. For a smoother experience, please ensure you are logged into the Roblox app beforehand.","red","screen")
                    self.setdat["rejoin_method"] = "new tab"
                    continue
            #find hive
            time.sleep(2)
            mouse.click()
            self.keyboard.press("space")
            self.keyboard.walk("w",5+(i*0.5),0)
            self.keyboard.walk("s",0.3,0)
            self.keyboard.walk("d",5,0)
            self.keyboard.walk("s",0.3,0)
            time.sleep(0.5)
            hiveNumber = self.setdat["hive_number"]
            #find the hive in hive number
            self.logger.webhook("",f'Claiming hive {hiveNumber} (guessing hive location)', "dark brown")
            steps = round(hiveNumber*2.5) if hiveNumber != 1 else 0
            for _ in range(steps):
                self.keyboard.walk("a",0.4, 0)

            def findHive():
                self.keyboard.walk("a",0.4)
                #$time.sleep(0.15)
                if self.isBesideEImage("claimhive"):
                    self.keyboard.press("e")
                    return True
                return False
            rejoinSuccess = False
            for _ in range(3):
                if findHive():
                    self.logger.webhook("",f'Claimed hive {hiveNumber}', "bright green", "screen")
                    rejoinSuccess = True
                    break 
            #find a new hive
            else:
                self.logger.webhook("",f'Hive is {hiveNumber} already claimed, finding new hive','dark brown', "screen")
                #walk closer to the hives so the player wont walk up the ramp
                self.keyboard.walk("w",0.3,0)
                self.keyboard.walk("d",0.9*(hiveNumber)+2,0)
                self.keyboard.walk("s",0.3,0)
                time.sleep(0.5)
                for j in range(40):
                    if findHive():
                        guessedSlot = max(1,min(6, round((j+1)//2.5)))
                        hiveClaim = guessedSlot
                        if  1 < guessedSlot < 6:
                            hiveClaim += 1
                        self.logger.webhook("",f"Claimed hive {hiveClaim}", "bright green", "screen")
                        rejoinSuccess = True
                        self.setdat["hive_number"] = hiveClaim
                        break
            #after hive is claimed, convert
            if rejoinSuccess:
                time.sleep(1)
                self.convert()
                #no need to reset
                self.canDetectNight = True
                return
            self.logger.webhook("",f'Rejoin unsuccessful, attempt {i+2}','dark brown', "screen")
    
    def blueTextImageSearch(self, text, threshold=0.7):
        target = self.adjustImage("./images/blue", text)
        return locateImageOnScreen(target, self.mw*3/4, self.mh*2/3, self.mw//4,self.mh//3, threshold)
    #background thread for gather
    #check if mobs have been killed and reset their timings
    #check if player died
    def gatherBackground(self):
        field = self.status.value.split("_")[1]
        while self.isGathering:
            #death check
            st = time.time()
            if self.blueTextImageSearch("died"):
                self.died = True
            #mob respawn check
            self.setMobTimer(field)
            

    def gather(self, field):
        fieldSetting = self.fieldSettings[field]
        for i in range(3):
            #wait for bees to wake up
            time.sleep(3)
            #go to field
            self.cannon()
            self.logger.webhook("",f"Travelling: {field.title()}, Attempt {i+1}", "dark brown")
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
            self.logger.webhook("", f"Failed to land in field", "red")
            self.reset()
        else: #failed too many times
            return
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
        maxGatherTime = fieldSetting["mins"]*60
        gatherTimeLimit = "{:.2f}".format(fieldSetting["mins"])
        returnType = fieldSetting["return"]
        st = time.time()
        keepGathering = True
        self.died = False
        #time to gather
        self.status.value = f"gather_{field}"
        self.isGathering = True
        self.logger.webhook(f"Gathering: {field.title()}", f"Limit: {gatherTimeLimit} - {fieldSetting['shape']} - Backpack: {fieldSetting['backpack']}%", "light green")
        mouse.moveBy(10,5)
        gatherBackgroundThread = threading.Thread(target=self.gatherBackground)
        gatherBackgroundThread.daemon = True
        gatherBackgroundThread.start()
        self.keyboard.releaseMovement()
        def turnOffShitLock():
            if fieldSetting["shift_lock"]: self.keyboard.press('shift')
            self.moveMouseToDefault()

        if fieldSetting["shift_lock"]: self.keyboard.press('shift')
        while keepGathering:
            mouse.mouseDown()
            exec(open(f"../settings/patterns/{fieldSetting['shape']}.py").read())
            #cycle ends
            mouse.mouseUp()

            #check for gather interrupts
            if self.night and self.setdat["stinger_hunt"]: 
                #rely on task function in main to execute the stinger hunt
                turnOffShitLock()
                self.logger.webhook("Gathering: interrupted","Stinger Hunt","dark brown")
                self.reset(convert=False)
                break
            elif self.collectMondoBuff(gatherInterrupt=True):
                turnOffShitLock()
                break
            elif self.died:
                turnOffShitLock()
                self.logger.webhook("","Player died", "dark brown","screen")
                self.reset()
                break

            #check if max time is reached
            gatherTime = "{:.2f}".format((time.time() - st)/60)
            if time.time() - st > maxGatherTime:
                self.logger.webhook(f"Gathering: Ended", f"Time: {gatherTime} - Time Limit - Return: {returnType}", "light green", "honey-pollen")
                keepGathering = False
            #check backpack
            if bpc(self.mw, self.newUI) >= fieldSetting["backpack"]:
                self.logger.webhook(f"Gathering: Ended", f"Time: {gatherTime} - Backpack - Return: {returnType}", "light green", "honey-pollen")
                keepGathering = False

            #field drift compensation
            if fieldSetting["field_drift_compensation"]:
                self.fieldDriftCompensation.run()
        self.status.value = ""
        self.isGathering = False
        gatherBackgroundThread.join()
        #gathering was interrupted
        if keepGathering: 
            return
        else: turnOffShitLock()

        #go back to hive
        def walk_to_hive():
            nonlocal self
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
            self.canDetectNight = False
            self.logger.webhook("",f"Walking back to hive: {field.title()}", "dark brown")
            self.runPath(f"field_to_hive/{field}")
            #find hive and convert
            self.keyboard.walk("a", (self.setdat["hive_number"]-1)*0.9)
            self.keyboard.keyDown("a")
            st = time.time()
            self.canDetectNight = True
            while time.time()-st < 0.2*20:
                if self.isBesideEImage("makehoney"):
                    break
            self.keyboard.keyUp("a")
            #in case we overwalked
            time.sleep(0.25)
            for _ in range(4):
                if self.convert():
                    break
                self.keyboard.walk("d",0.2)
                time.sleep(0.2) #add a delay so that the E can popup
            else:
                self.logger.webhook("","Can't find hive, resetting", "dark brown", "screen")
                self.reset()

        if returnType == "reset":
            self.reset()
        elif returnType == "rejoin":
            self.rejoin()
        elif returnType == "whirligig":
            self.useItemInInventory("whirligig")
            if not self.convert():
                self.logger.webhook("","Whirligigs failed, walking to hive", "dark brown", "screen")
                walk_to_hive()
                return
            #whirligig sucessful
            self.reset(convert=False)
        elif returnType == "walk":
            walk_to_hive()

    #returns the coordinates of the keep old text
    def keepOldCheck(self):
        region = (self.ww/3.15,self.wh/2.15,self.ww/2.7,self.wh/4.2)
        res = ocr.customOCR(*region,0)
        multi = 1
        if self.display_type == "retina": multi = 2
        for i in res:
            if "keep" in i[1][0].lower() and "o" in i[1][0].lower():
                return ((i[0][0][0]+region[0])//multi, (i[0][0][1]+region[1])//multi)
        

    def antChallenge(self):
        self.logger.webhook("","Travelling: Ant Challenge","dark brown")
        self.cannon()
        self.runPath("collect/ant_pass_dispenser")
        self.keyboard.walk("w",3.5)
        self.keyboard.walk("a",3)
        self.keyboard.walk("d",3)
        self.keyboard.walk("s",0.4)
        time.sleep(0.5)
        if self.isBesideE(["spen","play"], ["need"]):
            self.logger.webhook("","Start Ant Challenge","bright green", "screen")
            self.keyboard.press("e")
            self.placeSprinkler()
            mouse.click()
            time.sleep(1)
            self.keyboard.walk("s",1.5)
            self.keyboard.walk("w",0.15)
            self.keyboard.walk("d",0.3)
            mouse.mouseDown()
            while True:
                keepOld = self.keepOldCheck()
                if keepOld is not None:
                    mouse.mouseUp()
                    self.logger.webhook("","Ant Challenge Complete","bright green", "screen")
                    time.sleep(1.5)
                    mouse.moveTo(*keepOld)
                    mouse.click()
                    breakLoop = True
                    break
            return
        self.logger.webhook("", "Cant start ant challenge", "red", "screen")

    def collectMondoBuff(self, gatherInterrupt = False):
        self.status.value = ""
        #check if mondo can be collected (first 10mins)
        current_time = datetime.now().strftime("%H:%M:%S")
        _,minute,_ = [int(x) for x in current_time.split(":")]
        #set respawn time to 20mins
        #mostly just to prevent the macro from going to mondo over and over again for the 10mins
        if minute > 10 or self.hasRespawned("mondo", 20*60): return False
        if gatherInterrupt:
            self.logger.webhook("Gathering: interrupted","Mondo Buff","dark brown")
            self.reset()
        st = time.perf_counter()
        self.logger.webhook("","Travelling: Mondo Buff","dark brown")
        #go to mondo buff
        self.cannon()
        self.keyboard.press("e")
        sleep(2.5)
        self.keyboard.walk("w",1.4)
        self.keyboard.walk("d",4)
        #wait
        self.saveTiming("mondo")
        self.logger.webhook("","Collecting: Mondo Buff","bright green", "screen")
        sleep(self.setdat["mondo_buff_wait"]*60)
        self.logger.webhook("","Collected: Mondo Buff","dark brown")
        self.reset(convert=True)
        #done
        return True

    def collectStickerPrinter(self):
        reached = False
        for _ in range(2):
            self.logger.webhook("",f"Travelling: Sticker Printer","dark brown")
            self.cannon()
            self.runPath("collect/sticker_printer")
            for _ in range(6):
                self.keyboard.walk("w", 0.2)
                reached = self.isBesideE(["inspect", "stick", "print"])
                if reached: break
            if reached: break
            self.logger.webhook("", f"Failed to reach sticker printer", "dark brown", "screen")
            self.reset(convert=False)
        else: return

        self.keyboard.press("e")
        #claim sticker
        eggPosData = {
            "basic": -95, 
            "silver": -40,
            "gold": 15,
            "diamond": 70,
            "mythic": 125
        }
        #click egg
        time.sleep(2)
        eggPos = eggPosData[self.setdat["sticker_printer_egg"]]
        mouse.moveTo(self.mw//2+eggPos, 4*self.mh//10-20)
        time.sleep(0.2)
        mouse.click()
        time.sleep(1)
        #check if on cooldown
        confirmImg = self.adjustImage("./images/menu", "confirm")
        if not locateImageOnScreen(confirmImg, self.mw//2+150, 4*self.mh//10+160, 120, 60, 0.7):
            self.logger.webhook(f"", "Sticker printer on cooldown", "dark brown", "screen")
            self.keyboard.press("e")
            self.saveTiming("sticker_printer")
            return
        #confirm
        mouse.moveTo(self.mw//2+225, 4*self.mh//10+195)
        time.sleep(0.1)
        mouse.click()
        time.sleep(0.2)
        mouse.moveBy(0, 3)
        time.sleep(0.1)
        mouse.click()
        time.sleep(0.2)
        #click yes
        self.clickYes()
        #wait for sticker to generate
        time.sleep(7)
        self.logger.webhook(f"", "Claimed sticker", "bright green", "sticker")
        self.saveTiming("sticker_printer")
        #close the inventory
        time.sleep(1)
        self.toggleInventory()


    def collect(self, objective):
        reached = None
        objectiveData = collectData[objective]
        displayName = objective.replace("_"," ").title()
        self.location = "collect"
        #go to collect and check that player has reached
        for i in range(3):
            self.logger.webhook("",f"Travelling: {displayName}","dark brown")
            self.cannon()
            self.runPath(f"collect/{objective}")
            if objectiveData[1] is None:
                reached = self.isBesideE(objectiveData[0])
            else:
                for _ in range(6):
                    self.keyboard.walk(objectiveData[1], 0.2)
                    reached = self.isBesideE(objectiveData[0])
                    if reached: break
            if reached: break
            self.logger.webhook("", f"Failed to reach {displayName}", "dark brown", "screen")
            if i != 2: self.reset(convert=False)
        
        if not reached: return #player failed to reach objective
        #player has reached, get cooldown info
        #check if on cooldown
        cooldownSeconds = objectiveData[2]
        if "(" and ":" in reached:
            closePos = reached.find(")")
            #get cooldown if close bracket is present or not
            if closePos >= 0:
                cooldownRaw = reached[reached.find("(")+1:closePos]
            else:
                cooldownRaw = reached.split("(")[1]

            #clean it up, extract only valid characters
            cooldownRaw = ''.join([x for x in cooldownRaw if x.isdigit() or x == ":" or x == "s"])
            cooldownSeconds = 0 #cooldown in seconds

            #check if its hour, mins or seconds
            if cooldownRaw.count(":") == 2: #hours
                hr, mins, s = [int(x) for x in cooldownRaw.split(":")]
                cooldownSeconds = hr*60*60 + mins*60 + s
            elif cooldownRaw.count(":") == 1: #mins
                mins, s = [int(x) for x in cooldownRaw.split(":")]
                cooldownSeconds = mins*60 + s
            elif "s" in cooldownRaw: #seconds
                cooldownSeconds = int(''.join([x for x in cooldownRaw if x.isdigit()]))

            cooldownFormat = timedelta(seconds=cooldownSeconds)
            self.logger.webhook("", f"{displayName} is on cooldown ({cooldownFormat} remaining)", "dark brown", "screen")
        else: #not on cooldown
            for _ in range(2):
                self.keyboard.press("e")
            #run the claim path (if it exists)
            self.runPath(f"collect/claim/{objective}", fileMustExist=False)
            time.sleep(0.1)
            self.logger.webhook("", f"Collected: {displayName}", "bright green", "screen")
        #update the internal cooldown
        self.saveTiming(objective)
        self.collectCooldowns[objective] = cooldownSeconds

    #accept mob and field and return them in the format used for timings.txt file
    #mob_field, eg ladybug_strawberry
    #werewolf is an acception, just return "werewolf"
    def formatMobTimingName(self, mob, field):
        if mob == "werewolf": return mob
        return f"{mob}_{field}"
    
    def hasMobRespawned(self, mob, field, timing = None):
        return self.hasRespawned(self.formatMobTimingName(mob, field), mobRespawnTimes[mob], True, timing)
    
    #to be used by the mob run walk paths
    #returns true if there are mobs in the field to be killed (enabled + respawned)
    #returns a list of mobs that have respawned
    def getRespawnedMobs(self, field):
        mobs = regularMobInFields[field]
        out = []
        for m in mobs:
            if self.setdat[m] and self.hasMobRespawned(m, field):
                out.append(m)
        return out
    
    #check which mobs have respawned in the field and reset their timings
    def setMobTimer(self, field):
        if not field in regularMobInFields: return
        timings = self.getTiming()
        mobs = regularMobInFields[field]
        for m in mobs:
            timingName = self.formatMobTimingName(m, field)
            #check respawn
            if self.hasMobRespawned(m, field, timings[timingName]):
                timings[timingName] = time.time()
        settingsManager.saveDict("./data/user/timings.txt", timings)

    #background thread function to determine if player has defeated the mob
    #time limit of 20s
    def mobRunAttackingBackground(self):
        st = time.time()
        while True:
            if self.blueTextImageSearch("died"):
                self.mobRunStatus = "dead"
                break
            elif self.blueTextImageSearch("defeated"):
                self.mobRunStatus = "looting"
                break
            elif time.time() - st > 20:
                self.mobRunStatus = "timeout"
                break
    #background thread to check if token link is collected or the macro runs out of time (max 15s)
    def mobRunLootingBackground(self):
        st = time.time()
        while time.time() - st < 20:
           if self.blueTextImageSearch("tokenlink"): break
        self.mobRunStatus = "done"

    def killMob(self, mob, field, walkPath = None):
        mobName = mob
        if mob == "rhinobeetle": mobName = "rhino beetle"
        self.status.value = "bugrun"
        self.logger.webhook("","{}: {} ({})".format("Travelling" if walkPath is None else "Walking", mobName.title(),field.title()),"dark brown")
        self.mobRunStatus = "attacking"
        attackThread = threading.Thread(target=self.mobRunAttackingBackground)
        attackThread.daemon = True
        if walkPath is None:
            #wait for bees to respawn
            time.sleep(10)
            self.cannon()
            self.goToField(field)
            #attack the mob
            attackThread.start()
        else:
            #attack the mob
            #attack thread will start in the path
            self.canDetectNight = False
            exec(walkPath)
            self.canDetectNight = True
        self.location = field
        self.logger.webhook("","Attacking: {} ({})".format(mobName.title(),field.title()),"dark brown")
        
        st = time.time()
        #move in squares to evade attacks
        #save the last entered side and front keys. This will be used for the looting pattern
        distance = 0.7
        lastSideKey = "d"
        lastFrontKey = "s"
        def dodgeWalk(k,t):
            nonlocal lastSideKey, lastFrontKey
            if k in ["w", "s"]: lastFrontKey = k
            elif k in ["a","d"]: lastSideKey = k
            self.keyboard.walk(k, t)
        while True:
            dodgeWalk("s", distance*1.2)
            if self.mobRunStatus != "attacking": break
            dodgeWalk("a", distance*1.8)
            if self.mobRunStatus != "attacking": break
            dodgeWalk("w", distance*1.2)
            if self.mobRunStatus != "attacking": break
            dodgeWalk("d", distance*1.8)
            if self.mobRunStatus != "attacking": break

        attackThread.join()
        if self.mobRunStatus == "dead":
            self.logger.webhook("","Player died", "dark brown","screen")
            return
        elif self.mobRunStatus == "timeout":
            self.setMobTimer(field)
            self.logger.webhook("","Could not kill {} in time. Maybe it hasn't respawned?".format(mobName.title()), "dark brown", "screen")
            return
        time.sleep(1.5)
        #loot
        self.logger.webhook("", "Looting: {}".format(mobName.title()), "bright green", "screen")
        #start another background thread to check for token link/time limit
        lootThread = threading.Thread(target=self.mobRunLootingBackground)
        lootThread.daemon = True
        lootThread.start()
        def lootPattern(f, s):
            if lastSideKey == "a":
                startSideKey = "d"
            elif lastSideKey == "d":
                startSideKey = "a"

            if lastFrontKey == "w":
                startFrontKey = "s"
            elif lastFrontKey == "s":
                startFrontKey = "w"

            while True:
                for _ in range(2):
                    self.keyboard.walk(startFrontKey, 0.72*f)
                    if self.mobRunStatus == "done": return
                    self.keyboard.walk(startSideKey, 0.1*s)
                    if self.mobRunStatus == "done": return
                    self.keyboard.walk(lastFrontKey, 0.72*f)
                    if self.mobRunStatus == "done": return
                    self.keyboard.walk(startSideKey, 0.1*s)
                    if self.mobRunStatus == "done": return
                for _ in range(2):
                    self.keyboard.walk(startFrontKey, 0.72*f)
                    if self.mobRunStatus == "done": return
                    self.keyboard.walk(lastSideKey, 0.1*s)
                    if self.mobRunStatus == "done": return
                    self.keyboard.walk(lastFrontKey, 0.72*f)
                    if self.mobRunStatus == "done": return
                    self.keyboard.walk(lastSideKey, 0.1*s)
                    if self.mobRunStatus == "done": return
        lootPattern(1.35, 2.5)
        self.setMobTimer(field)
        self.status.value = ""
        lootThread.join()
        #check if there are paths for the macro to walk to other fields for mob runs
        #run a path in the field format
        self.runPath(f"mob_runs/{field}", fileMustExist=False)

    def stingerHuntBackground(self):
        #find vic
        while not self.stopVic:
            #detect which field the vic is in
            if self.vicField is None:
                for field in self.vicFields:
                    if self.blueTextImageSearch(f"vic{field}"):
                        self.vicField = field
                        break
            else:
                if self.blueTextImageSearch("died"): self.died = True
            
            if self.blueTextImageSearch("vicdefeat"):
                self.vicStatus = "defeated"
                
    def stingerHunt(self):
        self.vicStatus = None
        self.vicField = None
        self.stopVic = False
        currField = None

        stingerHuntThread = threading.Thread(target=self.stingerHuntBackground)
        stingerHuntThread.daemon = True
        stingerHuntThread.start()
        class vicFoundException(Exception):
            pass
        for currField in self.vicFields:
            #go to field
            self.cannon()
            self.logger.webhook("",f"Travelling to {currField} (vicious bee)","dark brown")
            self.goToField(currField)

            for _ in range(4): #rotate 180. The vic patterns are from v1
                self.keyboard.press(".")
            
            #since we can't use break/return in an exec statement, use exceptions to terminate it early
            #walk in path
            #between each line of movement in the path, check if vic has been found
            pathLines = open(f"../settings/paths/vic/find_vic/{currField}.py").read().split("\n")
            pathCode = ""
            for code in pathLines:
                pathCode += f"{code}\n"
                if "self.keyboard.walk" in code or "sleep" in code:
                    pathCode += "if self.vicField is not None: raise vicFoundException\n"
            try:
                exec(pathCode)
            except vicFoundException:
                self.logger.webhook("",f"Vicious Bee detected ({self.vicField})", "dark brown") 
                break
            print(self.vicField)
            self.reset(convert=False)
        else: #unable to find vic
            self.stopVic = True
            stingerHuntThread.join()
            self.convert()
            return
        
        #kill vic
        def goToVicField():
            self.reset(convert=False)
            self.logger.webhook("",f"Travelling to {self.vicField} (vicious bee)","dark brown")
            self.goToField(currField)
            for _ in range(4): #rotate 180, as the vic patterns are from v1
                self.keyboard.press(".")

        #first, check if vic is found in the same field as the player
        if currField != self.vicField: goToVicField()
        
        #run the dodge pattern
        #similar to the search pattern, between each line of code, check if vic has been defeated/player died
        pathLines = open(f"../settings/paths/vic/kill_vic/{self.vicField}.py").read().split("\n")
        loop = True
        self.died = False
        st = time.time() 
        while loop:
            for code in pathLines:
                exec(code)
                #run checks
                if self.died or self.vicStatus is not None: break
            if self.vicStatus == "defeated":
                self.logger.webhook("","Vicious Bee Defeated","light green")
                break
            elif self.died:
                self.logger.webhook("","Player Died","dark brown")
                goToVicField()
                self.died = False
            elif time.time()-st > 180: #max 3 mins to kill vic
                self.logger.webhook("","Took too long to kill Vicious Bee","red", "screen")
                break
        self.stopVic = True
        stingerHuntThread.join()
        self.reset()

    def stumpSnail(self):
        self.cannon()
        self.logger.webhook("","Travelling: Stump Snail", "dark brown")
        self.goToField("stump")
        self.placeSprinkler()
        while True:
            mouse.click()
            keepOldData = self.keepOldCheck()
            if keepOldData is not None:
                mouse.mouseUp()
                break
        #handle the other stump snail
        self.logger.webhook("","Stump Snail Killed","bright green", "screen")
        self.saveTiming("stump_snail")
        def keepOld():
            time.sleep(0.5)
            mouse.moveTo(*keepOldData)
            mouse.click()

        def replace():
            replaceImg = self.adjustImage("./images/menu", "replace")
            res = locateImageOnScreen(replaceImg, self.mw/3.15,self.mh/2.15,self.mw/2.4,self.mh/4.2)
            if res is not None:
                mouse.moveTo(*res[1])
                mouse.click()
        amulet = self.setdat["stump_snail_amulet"]
        if amulet == "keep":
            keepOld()
        elif amulet == "replace":
            replace()
        elif amulet == "stop":
            while self.keepOldCheck(): mouse.click()
        elif amulet == "wait for command":
            self.status.value = "amulet_wait"
            #wait for user to send command to bot
            while self.status.value == "amulet_wait": mouse.click()
            if self.status.value == "amulet_keep":
                keepOld()
            elif self.status.value == "amulet_replace":
                replace()

    #sleep in ms, useful for implementing ahk code
    def msSleep(self, t):
        if t <= 0: return
        time.sleep(t/1000)

    #implementation of natro's nm_loot function
    def nmLoot(self, length, reps, dirKey):
        for _ in range(reps):
            self.keyboard.tileWalk("w", length)
            self.keyboard.tileWalk(dirKey, 1.5)
            self.keyboard.tileWalk("s", length)
            self.keyboard.tileWalk(dirKey, 1.5)

    def coconutCrabBackground(self):
        while self.bossStatus is None:
            if self.blueTextImageSearch("died"):
                self.died = True
            if self.blueTextImageSearch("coconutcrab_defeat", 0.8):
                self.bossStatus = "defeated"
        

    def coconutCrab(self):
        self.bossStatus = None
        cocoThread = threading.Thread(target=self.coconutCrabBackground)
        cocoThread.daemon = True
        cocoThread.start()
        for _ in range(2):
            self.cannon()
            self.logger.webhook("","Travelling: Coconut Crab","dark brown")
            self.goToField("coconut")
            for _ in range(4):
                self.keyboard.press(".")
            self.keyboard.walk("s", 1)
            self.keyboard.walk("d", 3)
            self.died = False
            self.bossStatus = None
            st = time.time()
            while True:
                mouse.mouseDown()
                #simplified version of natro's coco crab pattern
                for i in range(2):
                    self.keyboard.walk("a",6, False)
                    self.keyboard.walk("d",6-i*1.8, False)
                self.keyboard.walk("s",2)
                time.sleep(4.5)
                self.keyboard.walk("w",1)
                mouse.mouseUp()
                if time.time()-st > 900: #15min time limit
                    self.bossStatus = "timelimit"
                if self.died or self.bossStatus is not None: break
            
            if self.died:
                self.logger.webhook("", "Died to Coconut Crab", "dark brown")
                self.reset(convert=False)
                self.died = False
            elif self.bossStatus is not None:
                break
            
        if self.bossStatus == "timelimit":
            self.logger.webhook("", "Time Limit: Coconut Crab", "dark brown")
        elif self.bossStatus == "defeated":
            self.keyboard.walk("a", 2)
            self.logger.webhook("", "Defeated: Coconut Crab", "bright green", "screen")
            self.nmLoot(9, 4, "d")
            self.nmLoot(9, 4, "a")
            self.nmLoot(9, 4, "d")
            self.nmLoot(9, 4, "a")
            self.nmLoot(9, 4, "d")
            self.nmLoot(9, 4, "a")
        cocoThread.join()
        self.saveTiming("coconut_crab")
        self.reset()

    
    def goToPlanter(self, planter, field, method):
        global finalKey
        self.cannon()
        self.logger.webhook("", f"Travelling: {planter.title()} Planter ({field.title()})", "dark brown")
        self.goToField(field)
        #move from center of field to planter spot
        finalKey = None
        path = f"../settings/paths/planters/{field}.py"
        if os.path.isfile(path): #not all fields have a planter path
            exec(open(path).read())
        #go to the planter
        if method == "collect": #return true if the planter can be found
            if finalKey is not None:
                st = time.time()
                while time.time()-st < (finalKey[1]+1):
                    self.keyboard.walk(finalKey[0],0.25)
                    if self.isBesideEImage("ebutton"): return True
            elif self.isBesideEImage("ebutton"):
                return True
            return False
        else: #place, just walk there
            if finalKey is not None: self.keyboard.walk(finalKey[0], finalKey[1])
            return True
    
    #place the planter and return the time it would take for the planter to grow (in secs)
    def placePlanter(self, planter, field, harvestFull, glitter):
        self.goToPlanter(planter, field, "place")
        name = planter.lower().replace(" ","").replace("-","")
        if glitter: self.useItemInInventory("glitter") #use glitter
        if not self.useItemInInventory(f"{name}planter"):
            return 
        self.logger.webhook("",f"Placed Planter: {planter.title()}", "dark brown", "screen")
        #calculate growth time. If the user didnt select harvest when full, return the harvest every X hours instead
        if harvestFull:
            baseGrowthTime, bonusFields, fieldGrowthBonus = planterGrowthData[planter]
            bonusTime = 0
            if glitter: bonusTime += 0.25
            if field in bonusFields: bonusTime += fieldGrowthBonus
            return (baseGrowthTime*(1-bonusTime))

        else:
            return self.setdat["manual_planters_collect_every"]*60*60 

    def collectPlanter(self, planter, field):
        if not self.goToPlanter(planter, field, "collect"):
            self.logger.webhook("",f"Unable to find Planter: {planter.title()}", "dark brown", "screen")
            return
        self.keyboard.press("e")
        self.clickYes()
        self.logger.webhook("",f"Looting: {planter.title()} planter","bright green", "screen")
        self.keyboard.multiWalk(["s","d"], 0.87)
        self.nmLoot(9, 5, "a")

    #iterate through all 3 slots in a cycle
    def placePlanterCycle(self, cycle):
        collectFull = self.setdat["manual_planters_collect_full"]
        planterGrowthMaxTime = 0
        planterData = { #planter data to be stored in a file
            "cycle": cycle,
            "planters": [],
            "fields": [],
            "gatherFields": [],
            "harvestTime": 0
        }
        for i in range(3):
            planter = self.setdat[f"cycle{cycle}_{i+1}_planter"]
            field = self.setdat[f"cycle{cycle}_{i+1}_field"]
            if planter == "none" or field == "none": continue #check that both the planter and field are present
            glitter = self.setdat[f"cycle{cycle}_{i+1}_glitter"]
            #set the cooldown for planters and place them
            planterGrowthTime = self.placePlanter(planter,field, collectFull, glitter)
            if not planterGrowthTime: #make sure the planter was placed
                self.reset()
                continue 
            #get the maximum planter growth time
            if planterGrowthTime > planterGrowthMaxTime:
                planterGrowthMaxTime = planterGrowthTime
            planterData["planters"].append(planter)
            planterData["fields"].append(field)
            #set which fields to gather in
            if self.setdat[f"cycle{cycle}_{i+1}_gather"]: 
                planterData["gatherFields"].append(field)
            self.reset()

        planterData["harvestTime"] = time.time() + planterGrowthMaxTime
        #convert planter growth max time to hrs, mins, secs readable format
        planterReady = time.strftime("%H:%M:%S", time.gmtime(planterGrowthMaxTime))
        self.logger.webhook("", f"Planters will be ready in: {planterReady}", "light blue")
        
        #save the planter data
        with open("./data/user/manualplanters.txt", "w") as f:
            f.write(str(planterData))
        f.close()
    
    
    def start(self):
        #if roblox is not open, rejoin
        if not appManager.openApp("roblox"):
            self.rejoin()
        else:
            #toggle fullscreen
            if not self.isFullScreen():
                self.toggleFullScreen()
        #disable game mode
        self.moveMouseToDefault()
        if sys.platform == "darwin":
            time.sleep(1)
            #check roblox scaling
            #this is done by checking if all pixels at the top of the screen are black
            topScreen = mssScreenshot(0, 0, self.mw, 2)
            extrema = topScreen.convert("L").getextrema()
            #all are black
            if extrema == (0, 0):
                messageBox.msgBox(text='It seems like you have not enabled roblox scaling. The macro will not work properly.\n1. Close Roblox\n2. Go to finder -> applications -> right click roblox -> get info -> enable "scale to fit below built-in camera"', title='Roblox scaling')
            #make sure game mode is a feature (macOS 14.0 and above and apple chips)
            macVersion, _, _ = platform.mac_ver()
            macVersion = float('.'.join(macVersion.split('.')[:2]))
            if macVersion >= 14 and platform.processor() == "arm":
                self.logger.webhook("","Disabling game mode","dark brown")
                #make sure roblox is not fullscreen
                self.toggleFullScreen()
                    
                #find the game mode button
                lightGameMode = self.adjustImage("./images/mac", "gamemodelight")
                darkGameMode = self.adjustImage("./images/mac", "gamemodedark")
                x = self.mw/2.3
                time.sleep(1.2)
                #find light mode
                res = locateImageOnScreen(lightGameMode,x, 0, self.mw-x, 60, 0.7)
                if res is None: #cant find light, find dark
                    res = locateImageOnScreen(darkGameMode,x, 0, self.mw-x, 60, 0.7)
                #found either light or dark
                if not res is None:
                    gx, gy = res[1]
                    if self.display_type == "retina":
                        gx //= 2
                        gy //= 2
                    mouse.moveTo(gx+x, gy)
                    time.sleep(0.1)
                    mouse.fastClick()
                    time.sleep(0.5)
                    #check if game mode is enabled
                    screen = mssScreenshot(x, 0, self.mw-x, 150)
                    ocrRes = ocr.ocrRead(screen)
                    for i in ocrRes:
                        if "mode off" in i[1][0].lower():
                            #disable game mode
                            bX, bY = ocr.getCenter(i[0])
                            if self.display_type == "retina":
                                bX //= 2
                                bY //= 2
                            mouse.moveTo(x+bX, bY)
                            mouse.click()                        
                            break
                    else: #game mode is already disabled/couldnt be found
                        mouse.moveTo(x+gx, gy)
                        mouse.click()
                #fullscreen back roblox
                appManager.openApp("roblox")
                self.toggleFullScreen()
            time.sleep(1)
            self.moveMouseToDefault()

        #detect new/old ui and set 
        #also check for screen recording permission 
        if self.getTop(0):
            self.newUI = False
            self.logger.webhook("","Detected: Old Roblox UI","light blue")
        elif self.getTop(30):
            self.newUI = True
            self.logger.webhook("","Detected: New Roblox UI","light blue")
            ocr.newUI = True
        else:
            self.logger.webhook("","Unable to detect Roblox UI","red", "screen")
            self.newUI = False   
            #2nd check for screen recording perms by checking for sprinkler icon
            if sys.platform == "darwin":
                sprinklerImg = self.adjustImage("./images/menu", "sprinkler")
                if not locateImageOnScreen(sprinklerImg, self.mw//2-300, self.mh*3/4, 300, self.mh*1/4, 0.75):
                    messageBox.msgBox(text='It seems like terminal does not have the screen recording permission. The macro will not work properly.\n\nTo fix it, go to System Settings -> Privacy and Security -> Screen Recording -> add and enable Terminal.\n\nVisit #6system-settings in the discord for more detailed instructions', title='Screen Recording Permission')

        #check for accessibility
        #this is done by taking 2 different screenshots
        #if they are both the same, we assume that the keypress didnt go through and hence accessibility is not enabled
        if sys.platform == "darwin":
            img1 = pillowToHash(mssScreenshot())
            self.keyboard.press("esc")
            time.sleep(0.1)
            time.sleep(0.5)
            img2 = pillowToHash(mssScreenshot())
            self.keyboard.press("esc")
            if similarHashes(img1, img2, 3):
                messageBox.msgBox(text='It seems like terminal does not have the accessibility permission. The macro will not work properly.\n\nTo fix it, go to System Settings -> Privacy and Security -> Accessibility -> add and enable Terminal.\n\nVisit #6system-settings in the discord for more detailed instructions', title='Accessibility Permission')


        #enable night detection
        if self.setdat["stinger_hunt"]:
            nightDetectThread = threading.Thread(target=self.detectNight)
            nightDetectThread.daemon = True
            nightDetectThread.start()
        self.reset(convert=True)
        self.saveTiming("rejoin_every")
