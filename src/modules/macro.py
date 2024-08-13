import modules.screen.ocr as ocr
from modules.screen.pixelColor import getPixelColor
import modules.misc.appManager as appManager
import modules.misc.settingsManager as settingsManager
import time
import pyautogui as pag
from modules.screen.screenshot import mssScreenshot
from modules.controls.keyboard import keyboard
from modules.controls.sleep import sleep
import modules.controls.mouse as mouse
from modules.screen.screenData import getScreenData
import modules.logging.log as logModule
from operator import itemgetter
import sys
import os
import numpy as np
from threading import Thread
from modules.screen.backpack import bpc
from modules.screen.imageSearch import locateImageOnScreen
import webbrowser
from pynput.keyboard import Key, Controller
import cv2
pynputKeyboard = Controller()
class macro:
    def __init__(self, status, log):
        self.status = status
        self.setdat = settingsManager.loadAllSettings()
        self.fieldSettings = settingsManager.loadFields()
        self.mw, self.mh = pag.size()
        screenData = getScreenData()
        self.display_type, self.ww, self.wh, self.ysm, self.xsm, self.ylm, self.xlm = itemgetter("display_type", "screen_width","screen_height", "y_multiplier", "x_multiplier", "y_length_multiplier", "x_length_multiplier")(screenData)
        self.keyboard = keyboard(self.setdat["movespeed"]) #TODO: implement haste compensation
        self.logger = logModule.log(log, self.setdat["enable_webhook"], self.setdat["webhook_link"])

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
        print(text)
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
    
    def clickYes(self):
        yesImg = cv2.imread(f"./images/{self.display_type}/inventory/yes.png")
        x = self.ww/3.2
        y = self.wh/2.3
        time.sleep(0.4)
        _, max_val, _, max_loc = locateImageOnScreen(yesImg,x,y,self.ww/2.5,self.wh/3.4)
        bestX, bestY = max_loc
        if self.display_type == "retina":
            bestX //=2
            bestY //=2
        mouse.teleport(bestX+x, bestY+y)
        time.sleep(0.5)
        for _ in range(2):
            mouse.click()

    def useItemInInventory(self, itemName):
        itemImg = cv2.imread(f"./images/{self.display_type}/inventory/{itemName}.png")
        def toggleInventory():
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
        #open inventory
        toggleInventory()
        time.sleep(0.3)
        self.keyboard.press("s")
        #scroll down, note the best match
        bestScroll, bestX, bestY = None, None, None
        valBest = 0
        for i in range(20):
            min_val, max_val, min_loc, max_loc = locateImageOnScreen(itemImg, 0, 80, 100, self.mh-120)
            print(max_val)
            if max_val > valBest:
                valBest = max_val
                bestX, bestY = max_loc
                bestScroll = i
            for j in range(4):
                pynputKeyboard.press(Key.page_down)
                pynputKeyboard.release(Key.page_down)
                if j > 1: time.sleep(0.05)
        #scroll to the top
        for _ in range(100):
            pynputKeyboard.press(Key.page_up)
            pynputKeyboard.release(Key.page_up)
        time.sleep(0.1)
        #scroll to item
        for _ in range(bestScroll*4):
            pynputKeyboard.press(Key.page_down)
            pynputKeyboard.release(Key.page_down)
        #close UI navigation
        self.keyboard.press("\\")
        if self.display_type == "retina":
            mouse.teleport(bestX//2+20, bestY//2+80+20)
        else:
            mouse.teleport(bestX+20, bestY+80+20)
        mouse.click()
        self.clickYes()
        #close inventory
        toggleInventory()
        #close UI navigation
        self.keyboard.press("\\")

    def convert(self, bypass = False):
        if not bypass:
            if not self.isBesideE(["make", "маке"], ["to"]): return False
        self.logger.webhook("", "Converting", "brown", True)
        self.keyboard.press("e")
        st = time.time()
        time.sleep(2)
        while self.isBesideE(["stop"]): pass
        #deal with the extra delay
        self.logger.webhook("", "Finished converting", "brown")
        wait = self.setdat["convert_wait"]
        if (wait):
            self.logger.webhook("", f'Waiting for an additional {wait} seconds', "light green")
        time.sleep(wait)
        return True

    def reset(self, hiveCheck = False, convert = True):
        self.keyboard.releaseMovement()
        yOffset = 10 #calculate yoffset
        if self.newUI: yOffset += 20
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
            self.logger.webhook("Notice", f"Unable to detect that player respawned at hive, continuing", "red", True)
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
        self.logger.webhook("Notice", f"Unable to detect the direction the player is facing, continuing", "red", True)
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
            self.logger.webhook("Notice", f"Could not find cannon", "dark brown")
            self.reset()
        else:
            self.logger.webhook("Notice", f"Failed to reach cannon too many times", "red")
    
    def rejoin(self):
        rejoinMethod = self.setdat["rejoin_method"]
        psLink = self.setdat["private_server_link"]
        browserLink = "https://www.roblox.com/games/4189852503?privateServerLinkCode=87708969133388638466933925137129"
        for i in range(3):
            if psLink and i ==2: 
                self.logger.webhook("", "Failed rejoining too many times, falling back to a public server", "red", True)
            else:
                browserLink = psLink
            appManager.closeApp("Roblox") # close roblox
            time.sleep(4)
            #execute rejoin method
            if rejoinMethod == "deeplink":
                deeplink = "roblox://placeID=1537690962"
                if psLink:
                    deeplink += f"&linkCode={psLink.lower().split('code=')[1]}"
                print(deeplink)
                appManager.openDeeplink(deeplink)
            elif rejoinMethod == "new tab":
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
            time.sleep(self.setdat["rejoin_wait"])
            appManager.openApp("roblox")
            #run fullscreen check (mac only)
            if sys.platform == "darwin":
                menubarRaw = ocr.customOCR(0, 0, 300, 60, 0) #get menu bar
                menubar = ""
                try:
                    for x in menubarRaw:
                        menubar += x[1][0]
                except:
                    pass
                menubar = menubar.lower()
                if "rob" in menubar or "lox" in menubar: #check if roblox can be found in menu bar
                    self.logger.webhook("","Roblox is not in fullscreen, activating fullscreen", "dark brown")
                    self.keyboard.keyDown("command")
                    time.sleep(0.05)
                    self.keyboard.keyDown("ctrl")
                    time.sleep(0.05)
                    self.keyboard.keyDown("f")
                    time.sleep(0.1)
                    self.keyboard.keyUp("command")
                    self.keyboard.keyUp("ctrl")
                    self.keyboard.keyUp("f")
                else:
                    self.logger.webhook("","Roblox is already in fullscreen, not activating fullscreen", "dark brown")

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
            #find hive
            self.keyboard.walk("w",5+(i*0.5),0)
            self.keyboard.walk("s",0.3,0)
            self.keyboard.walk("d",4,0)
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
                time.sleep(0.15)
                if self.isBesideE(["claim", "hive"]):
                    self.logger.press("e")
                    return True
                return False
            rejoinSuccess = False
            for _ in range(3):
                if findHive():
                    self.logger.webhook("",f'Claimed hive {hiveNumber}', "bright green",True)
                    rejoinSuccess = True
                    break 
            #find a new hive
            else:
                self.logger.webhook("",f'Hive is {hiveNumber} already claimed, finding new hive','dark brown', True)
                self.keyboard.walk("d",0.9*(hiveNumber)+1,0)
                time.sleep(0.5)
                for j in range(40):
                    if findHive():
                        hiveClaim = max(1,min(6,round((j+1)//2.5)))
                        self.logger.webhook("",f"Claimed hive {hiveClaim}", "bright green", True)
                        rejoinSuccess = True
                        break
            #after hive is claimed, convert
            if rejoinSuccess:
                self.convert()
                #no need to reset
                #TODO: haste compensation
                return
            self.logger.webhook("",f'Rejoin unsuccessful, attempt {i+2}','dark brown', True)


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
        maxGatherTime = fieldSetting["mins"]*60
        gatherTimeLimit = "{:.2f}".format(fieldSetting["mins"])
        returnType = fieldSetting["return"]
        st = time.time()
        keepGathering = True
        #time to gather
        self.logger.webhook(f"Gathering: {field.title()}", f"Limit: {gatherTimeLimit} - {fieldSetting['shape']} - Backpack: {fieldSetting['backpack']}%", "light green")
        mouse.moveBy(10,5)
        while keepGathering:
            if fieldSetting["shift_lock"]: self.keyboard.press('shift')
            mouse.mouseDown()
            exec(open(f"../settings/patterns/{fieldSetting['shape']}.py").read())
            #cycle ends
            mouse.mouseUp()
            if fieldSetting["shift_lock"]: self.keyboard.press('shift')
            #check if max time is reached
            gatherTime = "{:.2f}".format(time.time() - st)
            if time.time() - st > maxGatherTime:
                self.logger.webhook(f"Gathering: Ended", f"Time: {gatherTime} - Time Limit - Return: {returnType}", "light green")
                keepGathering = False
            #check backpack
            if bpc(self.ww, self.newUI, self.display_type) >= fieldSetting["backpack"]:
                self.logger.webhook(f"Gathering: Ended", f"Time: {gatherTime} - Backpack - Return: {returnType}", "light green")
                keepGathering = False
        
        #go back to hive
        def walk_to_hive():
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
                time.sleep(0.2) #add a delay so that the E can popup
                if self.isBesideE(["make", "маке"]):
                    self.convert(bypass=True)
                    self.reset(convert=False)
                    break
            else:
                self.logger.webhook("","Can't find hive, resetting", "dark brown")
                self.reset()

        if returnType == "reset":
            self.reset()
        elif returnType == "rejoin":
            pass
        elif returnType == "whirligig":
            self.useItemInInventory("whirligig")
            if not self.convert():
                self.logger.webhook("","Whirligigs failed, walking to hive", "dark brown", True)
                walk_to_hive()
                return
            #whirligig sucessful
            self.reset(convert=False)
        elif returnType == "walk":
            walk_to_hive()

    def start(self):
        print(self.status.value)
        appManager.openApp("roblox")
        time.sleep(2)
        #detect new/old ui and set 
        if self.getTop(0):
            self.newUI = False
            self.logger.webhook("","Detected: Old Roblox UI","light blue")
        elif self.getTop(30):
            self.newUI = True
            self.logger.webhook("","Detected: New Roblox UI","light blue")
            ocr.newUI = True
        else:
            self.logger.webhook("","Unable to detect Roblox UI. Ensure that terminal has the screen recording permission","red", True)
            self.newUI = False   
        self.reset(convert=True)
