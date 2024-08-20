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
from modules.submacros.fieldDriftCompensation import fieldDriftCompensation
from operator import itemgetter
import sys
import os
import numpy as np
from threading import Thread
from modules.submacros.backpack import bpc
from modules.screen.imageSearch import locateImageOnScreen
import webbrowser
from pynput.keyboard import Key, Controller
import cv2
from datetime import timedelta, datetime
from modules.misc.imageManipulation import pillowToCv2
from PIL import Image
pynputKeyboard = Controller()

#data for collectable objectives
#[besideE text, movement key, max cooldowns]
collectData = { 
    "wealth_clock": [["use"], "w", 1*60*60], #1hr
    "blueberry_dispenser": [["use", "dispenser"], "a", 4*60*60], #4hr
    "strawberry_dispenser": [["use", "dispenser"], None, 4*60*60], #4hr
    "royal_jelly_dispenser": [["claim", "royal"], "a",22*60*60], #22hr
    "treat_dispenser": [["use", "treat"], "w", 1*60*60], #1hr
    "ant_pass_dispenser": [["use", "free"], None, 2*60*60], #2hr
    "glue_dispenser": [["use", "glue"], None, 22*60*60], #22hr
    "stockings": [["check", "inside", "stocking"], None, 1*60*60], #1hr
    "wreath": [["admire", "honey"], None, 30*60], #30mins
    "feast": [["dig", "beesmas"], "s", 1.5*60*60], #1.5hr
    "samovar": [["heat", "samovar"], "w", 6*60*60], #6hr
    "snow_machine": [["activate"], None, 2*60*60], #2hr
    "lid_art": [["gander", "onett", "art"], "s", 8*60*60], #8hr
    "candles": [["admire", "candle", "honey"], "w", 4*60*60] #4hr
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

    #resize the image based on the user's screen coordinates
    def adjustImage(self, path, imageName):
        #get a list of all images and find the name of the one that matches
        images = os.listdir(path)
        for x in images:
            #images are named in the format itemname-width
            #width is the width of the monitor used to take the image
            name, res = x.split(".")[0].split("-",1)
            if name == imageName:
                img = Image.open(f"{path}/{x}")
                break
        #get original size of image
        width, height = img.size
        #calculate the scaling value 
        #retina has 2x more, built-in is 1x
        if self.display_type == res:
            scaling = 1
        elif self.display_type == "built-in": #screen is built-in but image is retina
            scaling = 2
        else: #screen is retina but image is built-in
            scaling = 0.5
        #resize image
        img = img.resize((int(width/scaling), int(height/scaling)))
        #convert to cv2
        return pillowToCv2(img)
        
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
    
    def getTiming(self,name):
        return settingsManager.readSettingsFile("./data/user/timings.txt")[name]
    
    def saveTiming(self, name):
        return settingsManager.saveSettingFile(name, time.time(), "./data/user/timings.txt")
    #returns true if the cooldown is up
    #note that cooldown is in seconds
    def hasRespawned(self, name, cooldown):
        timing = self.getTiming(name)
        return time.time() - timing >= cooldown 

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
        if self.isInBlueTexts(["must", "standing"], ["cannot", "close"]):
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
        _, max_val, _, max_loc = locateImageOnScreen(yesImg,x,y,self.mw/2.5,self.mh/3.4)
        bestX, bestY = max_loc
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

    def useItemInInventory(self, itemName):
        itemImg = self.adjustImage("./images/inventory", itemName)
        #open inventory
        self.toggleInventory()
        time.sleep(0.3)
        self.keyboard.press("s")
        #scroll down, note the best match
        bestScroll, bestX, bestY = None, None, None
        valBest = 0
        for i in range(20):
            min_val, max_val, min_loc, max_loc = locateImageOnScreen(itemImg, 0, 80, 180, self.mh-120)
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
            mouse.moveTo(bestX//2+20, bestY//2+80+20)
        else:
            mouse.moveTo(bestX+20, bestY+80+20)
        for _ in range(2):
            mouse.click()
        mouse.moveBy(10,10)
        mouse.click()
        self.clickYes()
        #close inventory
        self.toggleInventory()
        #close UI navigation
        self.keyboard.press("\\")
        #adjust camera
        for _ in range(20):
            pynputKeyboard.press(Key.page_down)
            pynputKeyboard.release(Key.page_down)

        for _ in range(5):
            pynputKeyboard.press(Key.page_up)
            time.sleep(0.05)
            pynputKeyboard.release(Key.page_up)
            time.sleep(0.01)


    def convert(self, bypass = False):
        if not bypass:
            if not self.isBesideE(["make", "маке"], ["to", "pollen"]): return False
        self.keyboard.press("e")
        st = time.time()
        time.sleep(2)
        self.logger.webhook("", "Converting", "brown", "screen")
        while not self.isBesideE(["to", "pollen", "flower", "field"]): 
            mouse.click()
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
            self.logger.webhook("Notice", f"Unable to detect that player respawned at hive, continuing", "red", "screen")
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
                if convert and (("make" in besideE or "маке" in besideE) and not ("to" in besideE or "pollen" in besideE)):
                    self.convert(True)
                return True
            
            for _ in range(4):
                self.keyboard.press(".")
                time.sleep(0.05)
        time.sleep(0.3)
        self.logger.webhook("Notice", f"Unable to detect the direction the player is facing, continuing", "red", "screen")
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
            self.keyboard.walk("d",0.2)
            self.keyboard.walk("s",0.07)
            for _ in range(6):
                self.keyboard.walk("d",0.15)
                time.sleep(0.05)
                if self.isBesideE(["fire","red"]):
                    return
            self.logger.webhook("Notice", f"Could not find cannon", "dark brown", "screen")
            self.reset()
        else:
            self.logger.webhook("Notice", f"Failed to reach cannon too many times", "red")
    
    def rejoin(self):
        rejoinMethod = self.setdat["rejoin_method"]
        psLink = self.setdat["private_server_link"]
        browserLink = "https://www.roblox.com/games/4189852503?privateServerLinkCode=87708969133388638466933925137129"
        self.logger.webhook("","Rejoining", "dark brown")
        for i in range(3):
            if psLink and i ==2: 
                self.logger.webhook("", "Failed rejoining too many times, falling back to a public server", "red", "screen")
            else:
                browserLink = psLink
            appManager.closeApp("Roblox") # close roblox
            time.sleep(4)
            #execute rejoin method
            if rejoinMethod == "deeplink":
                deeplink = "roblox://placeID=1537690962"
                if psLink:
                    deeplink += f"&linkCode={psLink.lower().split('code=')[1]}"
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
                self.keyboard.walk("d",0.9*(hiveNumber)+1,0)
                time.sleep(0.5)
                for j in range(40):
                    if findHive():
                        hiveClaim = max(1,min(6,round((j+1)//2.5)))
                        self.logger.webhook("",f"Claimed hive {hiveClaim}", "bright green", "screen")
                        rejoinSuccess = True
                        break
            #after hive is claimed, convert
            if rejoinSuccess:
                self.convert()
                #no need to reset
                #TODO: haste compensation
                return
            self.logger.webhook("",f'Rejoin unsuccessful, attempt {i+2}','dark brown', "screen")


    def gather(self, field):
        fieldSetting = self.fieldSettings[field]
        for i in range(3):
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
            gatherTime = "{:.2f}".format((time.time() - st)/60)
            if time.time() - st > maxGatherTime:
                self.logger.webhook(f"Gathering: Ended", f"Time: {gatherTime} - Time Limit - Return: {returnType}", "light green", "honey-pollen")
                keepGathering = False
            #check backpack
            if bpc(self.ww, self.newUI, self.display_type) >= fieldSetting["backpack"]:
                self.logger.webhook(f"Gathering: Ended", f"Time: {gatherTime} - Backpack - Return: {returnType}", "light green", "honey-pollen")
                keepGathering = False
            #check for gather interrupts
            if self.collectMondoBuff(gatherInterrupt=True):
                return

            #field drift compensation
            if fieldSetting["field_drift_compensation"]:
                fieldDriftCompensation(self.display_type == "retina")
        
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
                self.logger.webhook("","Whirligigs failed, walking to hive", "dark brown", "screen")
                walk_to_hive()
                return
            #whirligig sucessful
            self.reset(convert=False)
        elif returnType == "walk":
            walk_to_hive()

    def antChallenge(self):
        self.logger.webhook("","Travelling: Ant Challenge","dark brown")
        self.cannon()
        self.runPath("collect/ant_pass")
        self.keyboard.walk("w",4)
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
            region = (self.ww/3.15,self.wh/2.15,self.ww/2.7,self.wh/4.2)
            multi = 1
            if self.display_type == "retina":
                multi = 2
            mouse.mouseDown()
            breakLoop = False
            while not breakLoop:
                res = ocr.customOCR(*region,0)
                for i in res:
                    if "keep" in i[1][0].lower():
                        mouse.mouseUp()
                        mouse.moveTo((i[0][0][0]+region[0])//multi, (i[0][0][1]+region[1])//multi)
                        mouse.click()
                        breakLoop = True
                        break
                    
            self.logger.webhook("","Ant Challenge Complete","bright green", "screen")
            return
        self.logger.webhook("", "Cant start ant challenge", "red", "screen")

    def collectMondoBuff(self, gatherInterrupt = False):
        #check if mondo can be collected (first 10mins)
        current_time = datetime.now().strftime("%H:%M:%S")
        hour,minute,_ = [int(x) for x in current_time.split(":")]
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
        eggPos = eggPosData[self.setdat["sticker_printer_egg"]]
        mouse.moveTo(self.mw//2+eggPos, 4*self.mh//10-20)
        time.sleep(0.2)
        mouse.click()
        time.sleep(0.2)
        #check if on cooldown
        confirmImg = self.adjustImage("./images/menu", "confirm")
        _, max_val, _, _ = locateImageOnScreen(confirmImg, self.mw//2+150, 4*self.mh//10+16, 100, 60)
        if max_val < 0.7:
            self.logger.webhook(f"", "Sticker printer on cooldown", "dark brown", "screen")
            self.keyboard.press("e")
            return
        #confirm
        mouse.moveTo(self.mw//2+225, 4*self.mh//10+195)
        time.sleep(0.1)
        mouse.click()
        time.sleep(0.2)
        #click yes
        self.clickYes()
        #wait for sticker to generate
        time.sleep(6)
        self.logger.webhook(f"", "Claimed sticker", "light green", "sticker")
        #close the inventory
        time.sleep(1)
        self.toggleInventory()
        self.keyboard.press("\\")


    def collect(self, objective):
        reached = None
        objectiveData = collectData[objective]
        displayName = objective.replace("_"," ").title()
        #go to collect and check that player has reached
        for _ in range(2):
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
            self.reset(convert=False)
        
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

            #clean it up, extract only valid values
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
            self.logger.webhook("", f"Collected: {displayName}", "light green", "screen")
        #update the internal cooldown
        self.saveTiming(objective)
        self.collectCooldowns[objective] = cooldownSeconds
        
    def start(self):
        #if roblox is not open, rejoin
        if not appManager.openApp("roblox"):
            self.rejoin()
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
            self.logger.webhook("","Unable to detect Roblox UI. Ensure that terminal has the screen recording permission","red", "screen")
            self.newUI = False   
        self.reset(convert=True)
