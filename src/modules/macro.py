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
    def __init__(self):
        self.setdat = settingsManager.loadAllSettings()
        self.fieldSettings = settingsManager.loadFields()
        self.mw, self.mh = pag.size()
        screenData = getScreenData()
        print(screenData)
        self.display_type, self.ww, self.wh, self.ysm, self.xsm, _, _ = itemgetter("display_type", "screen_width","screen_height", "y_multiplier", "x_multiplier", "y_length_multiplier", "x_length_multiplier")(screenData)
    def reset(self):
        yOffset = 0
        print("resetting")
        mouse.teleport(self.mw/(self.xsm*4.11)+40,(self.mh/(9*self.ysm))+yOffset)
        time.sleep(0.5)
        keyboard.press('esc')
        time.sleep(0.1)
        keyboard.press('r')
        keyboard.time.sleep(0.2)
    
    def start(self):
        appManager.openApp("roblox")
        time.sleep(3)
        self.reset()
