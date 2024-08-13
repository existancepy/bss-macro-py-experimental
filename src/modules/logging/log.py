import time
from modules.screen.screenshot import screenshotScreen
import modules.logging.webhook as logWebhook
from discord_webhook import DiscordWebhook
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
    def __init__(self, log, enableWebhook, webhookLink):
        self.logVar = log
        self.enableWebhook = enableWebhook
        self.webhookObj = DiscordWebhook(url = webhookLink)
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
            webhookImg = "webhookScreenshot"
            screenshotScreen(webhookImg)
        logWebhook.webhook(self.webhookObj, title, desc, logData["time"], colors[color], webhookImg)
        


    