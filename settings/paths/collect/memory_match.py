for _ in range(2):
    self.keyboard.press(",")
self.keyboard.press("e")
self.keyboard.keyDown("w")
sleep(0.8)
for _ in range(2):
    self.keyboard.press("space")
sleep(3)
for _ in range(2):
    self.keyboard.press(",")
sleep(1.9)
self.keyboard.press("space")
self.keyboard.keyUp("w")
sleep(0.3)
self.keyboard.walk("s",0.18)
self.keyboard.walk("a",0.4)