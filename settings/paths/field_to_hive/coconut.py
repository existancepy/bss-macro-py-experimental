self.keyboard.walk("d",4, False)
self.keyboard.walk("s",3)
self.keyboard.keyDown("s")
self.keyboard.slowPress('space')
time.sleep(0.2)
self.keyboard.keyUp("s")
self.keyboard.walk("s",5)
self.keyboard.keyDown("a")
time.sleep(4)
self.keyboard.keyUp("a")
self.keyboard.walk("w",4)

for i in range(3):
    self.keyboard.walk("d", 0.1)
    time.sleep(0.01)
    self.keyboard.walk("s", 0.1)
    time.sleep(0.01)
    self.keyboard.walk("a", 0.1)
    time.sleep(0.01)
    self.keyboard.walk("s", 0.1)
self.keyboard.press(".")
for i in range(3):
    self.keyboard.walk("d",0.1)
    self.keyboard.walk("w",0.2)
    
self.keyboard.walk("d",7)
self.keyboard.walk("w",1)
self.keyboard.multiWalk(["s","a"], 0.9)
self.keyboard.walk("d",0.25)




    
