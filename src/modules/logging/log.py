import time
from modules.screen.screenshot import screenshotScreen
import modules.logging.webhook as logWebhook
import threading
import pyautogui as pag

colors = {
    "red":"D22B2B",
    "light blue":"89CFF0",
    "bright green": "7CFC00",
    "light green": "98FB98",
    "dark brown": "5C4033",
    "brown": "D27D2D",
    "purple": "954cf5"   
}

mw, mh = pag.size()
screenshotRegions = {
    "screen": None,
    "honey-pollen": (mw/3.5, 0, mw/2.4, 40),
    "sticker": (200, 70, mw/2.5-200, mh/4),
}

def sendWebhook(url, title, desc, time, colorHex, ss = None):
    webhookImg = None
    if not ss is None:
        webhookImg = "webhookScreenshot.png"
        screenshotScreen("webhookScreenshot.png", screenshotRegions[ss])
    logWebhook.webhook(url, title, desc, time, colorHex, webhookImg)

class log:
    def __init__(self, log, enableWebhook, webhookURL):
        self.logVar = log
        self.enableWebhook = enableWebhook
        self.webhookURL = webhookURL
    #display in gui and in macrologs
    def log(self, msg):
        pass
    #webhook, gui and macrologs
    def webhook(self, title, desc, color, ss = None):
        #update logs
        logData = {
            "type": "webhook",
            "time": time.strftime("%H:%M:%S", time.localtime()),
            "title": title,
            "desc": desc,
            "color": colors[color]

        }
        self.logVar.value = str(logData)

        #send webhook
        #do it on a thread to avoid delays
        if self.enableWebhook: 
            webhookThread = threading.Thread(target=sendWebhook, args=(self.webhookURL, title, desc, logData["time"], colors[color], ss))
            webhookThread.start()
        
        #wait until main process has added the log to gui
        #while not self.logVar.value == "": pass
    
    def hourlyReport(self, title, desc, color):
        if not self.enableWebhook: return
        logWebhook.webhook(self.webhookURL, title, desc, time.strftime("%H:%M:%S", time.localtime()), colors[color], "hourlyReport.png")