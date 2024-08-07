import modules.screen.ocr as ocr
import pyautogui as pag
from modules.screen.pixelColor import getPixelColor
import modules.misc.appManager as appManager
import modules.misc.settingsManager as settingsManager
import time
import modules.controls.keyboard as keyboard
import modules.controls.mouse as mouse
from modules.screen.screenData import getScreenData
from operator import itemgetter

class macro:
    def __init__(self, status, log):
        self.status = status
        self.log = log
        self.setdat = settingsManager.loadAllSettings()
        self.fieldSettings = settingsManager.loadFields()
        self.mw, self.mh = pag.size()
        screenData = getScreenData()
        self.display_type, self.ww, self.wh, self.ysm, self.xsm, self.ylm, self.xlm = itemgetter("display_type", "screen_width","screen_height", "y_multiplier", "x_multiplier", "y_length_multiplier", "x_length_multiplier")(screenData)
    
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
            keyboard.press('esc')
            time.sleep(0.1)
            keyboard.press('r')
            keyboard.time.sleep(0.2)
            keyboard.press('enter')
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
                    keyboard.press("o")
                return True
            
            for _ in range(4):
                keyboard.press(".")
                time.sleep(0.05)
        time.sleep(0.3)
    
    def start(self):
        #TODO: detect new/old ui and set 
        appManager.openApp("roblox")
        time.sleep(2)
        self.reset()
