self.keyboard.slowPress("e")
sleep(0.52)
self.keyboard.keyDown("w")
self.keyboard.slowPress("space")
self.keyboard.slowPress("space")
sleep(5.35)
self.keyboard.keyUp("w")
time.sleep(2.2)
self.keyboard.walk("w", 1.7)


# foundGummyBee = False
# targetY = self.robloxWindow.mw/1.3
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
# for _ in range(int(3/0.02)):
#     self.keyboard.walk("w", 0.02)
#     screen = mssScreenshotNP(self.robloxWindow.mx, self.robloxWindow.my+100, self.robloxWindow.mw/2, self.robloxWindow.mh-200)
#     res = findColorObjectHSL(screen, [(270, 25, 20), (310, 80, 80)], kernel=kernel, best=2, draw=False)
#     if res:
#         res = max(res, key=lambda x: x[1])
#         if res[1]/2+100 >= targetY:
#             self.logger.webhook("","Aligned with gummy bee","dark brown", "screen")
#             foundGummyBee = True
#             break 
# else:
#     self.logger.webhook("Notice","Could not detect gummy bee's location","red", "screen")
#     foundGummyBee = False
#     #self.keyboard.walk("w",2.48)
self.keyboard.walk("w",1.037)
if True:
    itemCoords = self.findItemInInventory("gumdrops")
    if itemCoords is not None:
        self.keyboard.walk("a",1.4)
        self.keyboard.walk("w",0.15)
        self.keyboard.walk("a",0.3)
        time.sleep(0.3)
        self.keyboard.walk("w",0.1)
        self.useItemInInventory(x=itemCoords[0], y=itemCoords[1])
        self.canDetectNight = False #dont let night be detected inside gummy bear's lair
        time.sleep(2)
        self.keyboard.walk("w",2.5)
        time.sleep(0.5)
        self.canDetectNight = True

