import time as timeModule
import threading
import queue
from modules.screen.screenshot import screenshotRobloxWindow, mssScreenshot
import modules.logging.webhook as logWebhook
import mss
from modules.screen.robloxWindow import RobloxWindowBounds

colors = {
    "red": "D22B2B",
    "light blue": "89CFF0",
    "bright green": "7CFC00",
    "light green": "98FB98",
    "dark brown": "5C4033",
    "brown": "D27D2D",
    "purple": "954cf5",
    "orange": "FFA500",
    "white": "FFFFFF",
    "yellow": "FFFF00",
}
newUI = False
    

class webhookQueue:
    def __init__(self):
        self.queue = queue.Queue()
        self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.worker_thread.start()

    def _process_queue(self):
        while True:
            # Wait for a message from the queue
            data = self.queue.get()
            if data is None:
                print("Webhook queue stopped.")
                break
            # Send the webhook
            logWebhook.webhook(**data)
            self.queue.task_done()

    def add_to_queue(self, data):
        self.queue.put(data)

class log:
    def __init__(self, logQueue, enableWebhook, webhookURL, hourlyReportOnly=False, blocking=False, robloxWindow: RobloxWindowBounds = None):
        self.logQueue = logQueue
        self.webhookURL = webhookURL
        self.enableWebhook = enableWebhook
        self.blocking = blocking
        self.hourlyReportOnly = hourlyReportOnly
        self.robloxWindow = robloxWindow

        if not self.blocking:
            self.webhookQueue = webhookQueue()

    def log(self, msg):
        # Display in GUI or macro logs (to be implemented)
        pass

    def webhook(self, title, desc, color, ss=None, imagePath=None):
        # Update logs
        time = timeModule.strftime("%H:%M:%S", timeModule.localtime())
        logData = {
            "type": "webhook",
            "time": time,
            "title": title,
            "desc": desc,
            "color": colors[color]
        }
        self.logQueue.put(logData)

        print(f"[{time}] {title} {desc}")

        if not self.enableWebhook or self.hourlyReportOnly: return

        webhookImgPath = None
        if imagePath:
            webhookImgPath = imagePath
        elif ss:
            webhookImgPath = "webhookScreenshot.png"
            #if roblox window is not provided, make one
            if self.robloxWindow:
                robloxWindow = self.robloxWindow
            else:
                print("new window bounds")
                robloxWindow = RobloxWindowBounds()
                robloxWindow.setRobloxWindowBounds()

            screenshotRegions = {
                "screen": (robloxWindow.mx, robloxWindow.my, robloxWindow.mw, robloxWindow.mh),
                "honey-pollen": (robloxWindow.mx+robloxWindow.mw//2-320, robloxWindow.my+robloxWindow.yOffset, 650, 40),
                "sticker": (robloxWindow.mx+200, robloxWindow.my+70, 376, 225),
                "blue": (robloxWindow.mx+robloxWindow.mw*3/4, robloxWindow.my+robloxWindow.mh*2/3, robloxWindow.mw//4, robloxWindow.mh//3),
            }
            print(screenshotRegions["screen"])

            for _ in range(2):
                try:
                    mssScreenshot(*screenshotRegions[ss], save=True, filename=webhookImgPath)
                    break
                except mss.exception.ScreenShotError:
                    timeModule.sleep(0.5)
            else:
                webhookImgPath = None

        webhookData = {
            "url": self.webhookURL,
            "title": title,
            "desc": desc,
            "time": time,
            "color": colors[color],
            "imagePath": webhookImgPath
        }

        # Add the webhook message to the queue
        if self.blocking:
            logWebhook.webhook(**webhookData)
        else:
            self.webhookQueue.add_to_queue(webhookData)

    def hourlyReport(self, title, desc, color):
        if not self.enableWebhook: return
        logWebhook.webhook(self.webhookURL, title, desc, timeModule.strftime("%H:%M:%S", timeModule.localtime()), colors[color], "hourlyReport.png") 
