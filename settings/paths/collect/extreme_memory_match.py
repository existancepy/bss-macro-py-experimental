self.keyboard.walk("d", 4)
self.keyboard.walk("w", 1)
self.keyboard.keyDown("d")
self.keyboard.slowPress('space')
sleep(0.2)
self.keyboard.keyUp("d")
self.keyboard.keyDown("d")
time.sleep(2)
self.keyboard.slowPress('space')
sleep(0.2)
self.keyboard.keyUp("d")
self.keyboard.keyDown("w")
time.sleep(0.3)
self.keyboard.slowPress('space')
sleep(0.2)
self.keyboard.keyUp("w")
self.keyboard.walk("a",1)
self.keyboard.walk("w",3)

sleep(0.5)
self.keyboard.walk("d",2.5)
for _ in range(3):
    self.keyboard.keyDown("w")
    self.keyboard.slowPress('space')
    sleep(0.2)
    self.keyboard.keyUp("w")
    
self.keyboard.walk('w',2)
self.keyboard.keyDown("w")
self.keyboard.slowPress('space')
sleep(0.2)
self.keyboard.keyUp("w")
self.keyboard.walk('w',4)
self.keyboard.press(".")
self.keyboard.keyDown("w")
self.keyboard.slowPress('space')
sleep(0.2)
self.keyboard.keyUp("w")
self.keyboard.walk("w",1)
self.keyboard.press(".")
self.keyboard.walk("w",0.965)
self.keyboard.walk("d",0.3)
for i in range(5):
    if self.isBesideE(["spend", "play"]):
        self.keyboard.walk("s",0.2)
    else:
        break




    
