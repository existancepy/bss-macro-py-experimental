import time
from modules.screen.screenshot import screenshotScreen
import modules.logging.webhook as logWebhook
colors = {
    "red":"D22B2B",
    "light blue":"89CFF0",
    "bright green": "7CFC00",
    "light green": "98FB98",
    "dark brown": "5C4033",
    "brown": "D27D2D",
    "purple": "954cf5"
    
}

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
        if not self.enableWebhook: return
        webhookImg = None
        if ss:
            webhookImg = "webhookScreenshot.png"
            screenshotScreen(webhookImg)
        logWebhook.webhook(self.webhookURL, title, desc, logData["time"], colors[color], webhookImg)
        


    