self.keyboard.walk("s", 0.1)
self.keyboard.press("space")
self.keyboard.walk("a", 13, False)
self.keyboard.keyDown("w")
time.sleep(2)
self.keyboard.press("space")
time.sleep(3.5)
self.keyboard.keyUp("w")
self.keyboard.walk("a", 0.45, False)
self.keyboard.keyDown("w")
self.keyboard.press("space")
time.sleep(1.5)
self.keyboard.press("space")
time.sleep(3)
self.keyboard.keyUp("w")
self.keyboard.walk("a", 2.5, False)
self.keyboard.keyDown("w")
time.sleep(6)
self.keyboard.keyUp("w")
self.keyboard.walk("a", 1.2)
self.keyboard.walk("s", 6)