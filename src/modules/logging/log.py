import time
from modules.screen.screenshot import screenshotScreen
import modules.logging.webhook as logWebhook
import threading

colors = {
    "red":"D22B2B",
    "light blue":"89CFF0",
    "bright green": "7CFC00",
    "light green": "98FB98",
    "dark brown": "5C4033",
    "brown": "D27D2D",
    "purple": "954cf5"
    
}

def sendWebhook(url, title, desc, time, colorHex, ss):
    webhookImg = None
    if ss:
        webhookImg = "webhookScreenshot.png"
        screenshotScreen("webhookScreenshot.png")
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
    def webhook(self, title, desc, color, ss = False):
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
        if not self.enableWebhook: return
        webhookThread = threading.Thread(target=sendWebhook, args=(self.webhookURL, title, desc, logData["time"], colors[color], ss))
        webhookThread.start()
        


    