self.keyboard.slowPress("e")
sleep(0.52)
self.keyboard.keyDown("w")
self.keyboard.slowPress("space")
self.keyboard.slowPress("space")
sleep(5.35)
self.keyboard.keyUp("w")
time.sleep(2.2)
self.keyboard.walk("w",2.48)
self.keyboard.walk("a",1.32)
self.keyboard.walk("w",0.1)
self.keyboard.walk("a",0.2)
self.useItemInInventory("gumdrops")
self.canDetectNight = False #dont let night be detected inside gummy bear's lair
time.sleep(2)
self.keyboard.walk("w",2.5)
time.sleep(0.5)
self.canDetectNight = True

